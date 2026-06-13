"""Mini backend para el formulario de contacto de imationgroup.com.

Mismo patrón que autolinked-saas: FastAPI + SMTP via smtplib. Sin BD,
sin auth — solo recibe el formulario, valida, aplica rate-limit y manda
un correo a SUPPORT_EMAIL con Reply-To del visitante.
"""

import logging
import os
import smtplib
import time
from collections import deque
from email.message import EmailMessage
from threading import Lock
from typing import Deque, Dict

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("imationgroup-contact")


def env(name: str, default: str = "") -> str:
    return (os.getenv(name) or default).strip()


SMTP_HOST = env("SMTP_HOST")
SMTP_PORT = int(env("SMTP_PORT", "587"))
SMTP_USER = env("SMTP_USER")
SMTP_PASSWORD = env("SMTP_PASSWORD")
SMTP_FROM = env("SMTP_FROM", "info@imationgroup.com")
SMTP_USE_TLS = env("SMTP_USE_TLS", "true").lower() == "true"
SUPPORT_EMAIL = env("SUPPORT_EMAIL", "info@imationgroup.com")

ALLOWED_ORIGINS = [
    o.strip()
    for o in env(
        "ALLOWED_ORIGINS",
        "https://imationgroup.com,https://www.imationgroup.com,http://localhost:8080",
    ).split(",")
    if o.strip()
]


app = FastAPI(title="ImationGroup contact API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

# ── Blog (public + admin) ──────────────────────────────────────────────────
# Mounted at /blog and /<lang>/blog by nginx; /admin for the CMS.
from .blog.db import init_db as _blog_init_db  # noqa: E402
from .blog.routes_admin import router as blog_admin_router  # noqa: E402
from .blog.routes_public import lang_router, router as blog_public_router  # noqa: E402

_blog_init_db()
app.include_router(blog_public_router)
app.include_router(lang_router())
app.include_router(blog_admin_router)


@app.get("/api/health")
def health():
    return {"status": "ok", "smtp_configured": bool(SMTP_HOST)}


# ── Rate limit naïve (1 worker uvicorn es suficiente) ─────────────────────────
_RATE_WINDOW = 60 * 60   # 1 hora
_RATE_MAX = 5            # 5 envíos por IP/hora
_BUCKETS: Dict[str, Deque[float]] = {}
_LOCK = Lock()


def _allow(ip: str) -> bool:
    now = time.time()
    with _LOCK:
        bucket = _BUCKETS.setdefault(ip, deque())
        while bucket and bucket[0] < now - _RATE_WINDOW:
            bucket.popleft()
        if len(bucket) >= _RATE_MAX:
            return False
        bucket.append(now)
        return True


def _client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def send_email(to: str, subject: str, body: str, reply_to: str | None = None) -> bool:
    if not SMTP_HOST:
        log.warning("SMTP no configurado; correo NO enviado. to=%s subject=%r", to, subject)
        log.info("body: %s", body)
        return False

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM
    msg["To"] = to
    if reply_to:
        msg["Reply-To"] = reply_to
    msg.set_content(body)

    try:
        if SMTP_USE_TLS:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as s:
                s.starttls()
                if SMTP_USER:
                    s.login(SMTP_USER, SMTP_PASSWORD)
                s.send_message(msg)
        else:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20) as s:
                if SMTP_USER:
                    s.login(SMTP_USER, SMTP_PASSWORD)
                s.send_message(msg)
        log.info("email enviado to=%s subject=%r", to, subject)
        return True
    except Exception as e:  # noqa: BLE001
        log.exception("error enviando correo a %s: %s", to, e)
        return False


class ContactPayload(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    message: str = Field(min_length=4, max_length=4000)
    # Lengua del visitante para devolverle la confirmación en su idioma.
    lang: str | None = Field(default=None, max_length=8)
    # Honeypot — humanos no rellenan, los bots sí.
    website: str | None = None


# Confirmación al remitente — subject + body por idioma.
# Sin acuse de recibo, no hay manera de que la persona guarde lo que envió.
CONFIRMATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "subject": "We received your message — ImationGroup",
        "body": (
            "Hi {name},\n\n"
            "Thanks for reaching out to ImationGroup. We've received your message "
            "and will get back to you within 1-2 business days.\n\n"
            "For your records, here's a copy of what you sent:\n"
            "---------\n{message}\n---------\n\n"
            "Just reply to this email if anything else comes to mind — it goes "
            "straight to our team.\n\n"
            "— ImationGroup\ninfo@imationgroup.com"
        ),
    },
    "es": {
        "subject": "Hemos recibido tu mensaje — ImationGroup",
        "body": (
            "Hola {name},\n\n"
            "Gracias por contactar con ImationGroup. Hemos recibido tu mensaje y "
            "te responderemos en un plazo de 1-2 días laborables.\n\n"
            "Para tu referencia, aquí tienes una copia de lo que enviaste:\n"
            "---------\n{message}\n---------\n\n"
            "Si necesitas añadir algo, responde a este mismo correo — llegará "
            "directamente a nuestro equipo.\n\n"
            "— Equipo de ImationGroup\ninfo@imationgroup.com"
        ),
    },
    "gl": {
        "subject": "Recibimos a túa mensaxe — ImationGroup",
        "body": (
            "Ola {name},\n\n"
            "Grazas por contactar con ImationGroup. Recibimos a túa mensaxe e "
            "responderémosche en 1-2 días laborables.\n\n"
            "Para a túa referencia, aquí tes unha copia do que enviaches:\n"
            "---------\n{message}\n---------\n\n"
            "Se precisas engadir algo, responde a este mesmo correo — chegará "
            "directamente ao noso equipo.\n\n"
            "— Equipo de ImationGroup\ninfo@imationgroup.com"
        ),
    },
    "ca": {
        "subject": "Hem rebut el teu missatge — ImationGroup",
        "body": (
            "Hola {name},\n\n"
            "Gràcies per contactar amb ImationGroup. Hem rebut el teu missatge i "
            "et respondrem en un termini d'1-2 dies laborables.\n\n"
            "Per a la teva referència, aquí tens una còpia del que has enviat:\n"
            "---------\n{message}\n---------\n\n"
            "Si necessites afegir alguna cosa, respon a aquest mateix correu — "
            "arribarà directament al nostre equip.\n\n"
            "— Equip d'ImationGroup\ninfo@imationgroup.com"
        ),
    },
    "pt": {
        "subject": "Recebemos a sua mensagem — ImationGroup",
        "body": (
            "Olá {name},\n\n"
            "Obrigado por entrar em contacto com a ImationGroup. Recebemos a sua "
            "mensagem e responderemos em 1-2 dias úteis.\n\n"
            "Para sua referência, aqui está uma cópia do que enviou:\n"
            "---------\n{message}\n---------\n\n"
            "Se precisar de acrescentar algo, responda a este e-mail — irá "
            "directamente para a nossa equipa.\n\n"
            "— Equipa ImationGroup\ninfo@imationgroup.com"
        ),
    },
    "eu": {
        "subject": "Zure mezua jaso dugu — ImationGroup",
        "body": (
            "Kaixo {name},\n\n"
            "Eskerrik asko ImationGroup-ekin harremanetan jartzeagatik. Zure "
            "mezua jaso dugu eta 1-2 lanegunen barruan erantzungo dizugu.\n\n"
            "Zure erreferentziarako, hau da bidali zenuena:\n"
            "---------\n{message}\n---------\n\n"
            "Zerbait gehiago gehitu nahi baduzu, erantzun email honi — gure "
            "taldera zuzenean iritsiko da.\n\n"
            "— ImationGroup taldea\ninfo@imationgroup.com"
        ),
    },
    "et": {
        "subject": "Saime teie sõnumi kätte — ImationGroup",
        "body": (
            "Tere {name},\n\n"
            "Aitäh, et võtsite ImationGroup'iga ühendust. Saime teie sõnumi "
            "kätte ja vastame 1-2 tööpäeva jooksul.\n\n"
            "Teie tarbeks on siin koopia sellest, mida saatsite:\n"
            "---------\n{message}\n---------\n\n"
            "Kui soovite midagi lisada, vastake lihtsalt sellele e-kirjale — "
            "see jõuab otse meie meeskonnani.\n\n"
            "— ImationGroup meeskond\ninfo@imationgroup.com"
        ),
    },
}


def confirmation_for(lang: str | None) -> Dict[str, str]:
    """Return confirmation subject+body for the closest matching language."""
    if lang:
        code = lang.lower().split("-")[0]
        if code in CONFIRMATIONS:
            return CONFIRMATIONS[code]
    return CONFIRMATIONS["en"]


class ContactResponse(BaseModel):
    sent: bool


@app.post("/api/contact", response_model=ContactResponse)
def contact(payload: ContactPayload, request: Request):
    ip = _client_ip(request)

    if payload.website:
        log.info("[contact] honeypot rellenado, ignorando (ip=%s)", ip)
        return ContactResponse(sent=True)

    if not _allow(ip):
        log.warning("[contact] rate-limit alcanzado para ip=%s", ip)
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            "Has enviado demasiados mensajes. Inténtalo más tarde.",
        )

    name = payload.name.strip()
    sender_email = payload.email.strip()
    body = (
        "Nuevo mensaje desde el formulario de contacto de imationgroup.com\n\n"
        f"Nombre: {name}\n"
        f"Email:  {sender_email}\n"
        f"IP:     {ip}\n\n"
        "Mensaje:\n"
        "---------\n"
        f"{payload.message.strip()}\n"
    )
    subject = f"[Contacto web] {name}"

    ok = send_email(to=SUPPORT_EMAIL, subject=subject, body=body, reply_to=sender_email)
    if not ok:
        log.error("[contact] send_email devolvió False (ip=%s, from=%s)", ip, sender_email)

    # Confirmación al remitente — en su idioma cuando lo conocemos.
    # Si falla, NO falla el request: ya tenemos el mensaje principal en soporte.
    tpl = confirmation_for(payload.lang)
    confirm_ok = send_email(
        to=sender_email,
        subject=tpl["subject"],
        body=tpl["body"].format(name=name, message=payload.message.strip()),
        reply_to=SUPPORT_EMAIL,
    )
    if not confirm_ok:
        log.warning("[contact] confirmación al remitente falló (to=%s)", sender_email)

    return ContactResponse(sent=True)
