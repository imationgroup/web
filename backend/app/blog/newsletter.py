"""Newsletter: subscribe (double opt-in) + confirm + unsubscribe + send.

Public endpoints live on api.imationgroup.com under /api/newsletter/* and
/newsletter/<token> (the latter routed by nginx so the user clicks links
on the same domain as the email subject).
Sending happens from the contact backend's existing SMTP config -- no
new infra needed.
"""
from __future__ import annotations
import logging
import re
import secrets
import time
from collections import deque
from datetime import datetime, timezone
from email.message import EmailMessage
from threading import Lock
from typing import Deque, Dict, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, EmailStr, Field as PField
from sqlmodel import Session, select

from .config import DEFAULT_LANG, LANG_NAMES, LANGS, SITE_URL
from .db import engine, get_session
from .models import Post, Subscriber

log = logging.getLogger("imationgroup-newsletter")
router = APIRouter(tags=["newsletter"])

# ── localised email templates ──────────────────────────────────────────────
# Each entry = (subject, plain-text body). Body has placeholders:
#   {name}, {url}, {site}, {unsubscribe_url}, {title}, {excerpt}
CONFIRM_TEMPLATES = {
    "es": (
        "Confirma tu suscripción a ImationGroup",
        "Hola,\n\nGracias por suscribirte al boletín de ImationGroup. Para "
        "completar tu suscripción, confirma tu email haciendo click aquí:\n\n{url}\n\n"
        "Si no fuiste tú quien se suscribió, simplemente ignora este correo.\n\n"
        "— ImationGroup\ninfo@imationgroup.com",
    ),
    "gl": (
        "Confirma a túa subscrición a ImationGroup",
        "Ola,\n\nGrazas por subscribirte ao boletín de ImationGroup. Para completar a "
        "túa subscrición, confirma o teu email facendo click aquí:\n\n{url}\n\n"
        "Se non fuches ti, ignora este correo.\n\n— ImationGroup\ninfo@imationgroup.com",
    ),
    "ca": (
        "Confirma la teva subscripció a ImationGroup",
        "Hola,\n\nGràcies per subscriure't al butlletí d'ImationGroup. Per completar la "
        "teva subscripció, confirma el teu correu fent click aquí:\n\n{url}\n\n"
        "Si no vas ser tu, ignora aquest missatge.\n\n— ImationGroup\ninfo@imationgroup.com",
    ),
    "pt": (
        "Confirma a tua subscrição à ImationGroup",
        "Olá,\n\nObrigado por subscreveres a newsletter da ImationGroup. Para "
        "completar a tua subscrição, confirma o teu email aqui:\n\n{url}\n\n"
        "Se não foste tu, ignora este email.\n\n— ImationGroup\ninfo@imationgroup.com",
    ),
    "eu": (
        "Berretsi ImationGroup-en harpidetza",
        "Kaixo,\n\nEskerrik asko ImationGroup-en buletinera harpidetzeagatik. "
        "Harpidetza osatzeko, berretsi zure emaila esteka honetan:\n\n{url}\n\n"
        "Zuk ez baduzu egin, mesedez baztertu mezu hau.\n\n— ImationGroup\ninfo@imationgroup.com",
    ),
    "et": (
        "Kinnita oma ImationGroup'i tellimus",
        "Tere,\n\nTäname, et tellisid ImationGroup'i uudiskirja. Tellimuse "
        "kinnitamiseks klõpsa allolevat linki:\n\n{url}\n\n"
        "Kui Sa ei tellinud, ignoreeri seda kirja.\n\n— ImationGroup\ninfo@imationgroup.com",
    ),
    "en": (
        "Confirm your subscription to ImationGroup",
        "Hi,\n\nThanks for subscribing to ImationGroup's newsletter. To complete "
        "your subscription, confirm your email by clicking here:\n\n{url}\n\n"
        "If it wasn't you, just ignore this email.\n\n— ImationGroup\ninfo@imationgroup.com",
    ),
}

NEWSLETTER_TEMPLATES = {
    "es": (
        "{title} — ImationGroup",
        "Hola,\n\nHemos publicado un nuevo artículo en el blog de ImationGroup:\n\n"
        "{title}\n\n{excerpt}\n\nLee el artículo completo aquí:\n{url}\n\n"
        "— ImationGroup\n\n──────────\n"
        "¿No quieres recibir más correos? Date de baja: {unsubscribe_url}",
    ),
    "gl": (
        "{title} — ImationGroup",
        "Ola,\n\nPublicamos un novo artigo no blog de ImationGroup:\n\n"
        "{title}\n\n{excerpt}\n\nLe o artigo completo:\n{url}\n\n"
        "— ImationGroup\n\n──────────\n"
        "Non queres recibir máis correos? Date de baixa: {unsubscribe_url}",
    ),
    "ca": (
        "{title} — ImationGroup",
        "Hola,\n\nHem publicat un nou article al blog d'ImationGroup:\n\n"
        "{title}\n\n{excerpt}\n\nLlegeix l'article complet:\n{url}\n\n"
        "— ImationGroup\n\n──────────\n"
        "No vols rebre més correus? Dóna't de baixa: {unsubscribe_url}",
    ),
    "pt": (
        "{title} — ImationGroup",
        "Olá,\n\nPublicámos um novo artigo no blog da ImationGroup:\n\n"
        "{title}\n\n{excerpt}\n\nLê o artigo completo aqui:\n{url}\n\n"
        "— ImationGroup\n\n──────────\n"
        "Não queres receber mais? Cancela a subscrição: {unsubscribe_url}",
    ),
    "eu": (
        "{title} — ImationGroup",
        "Kaixo,\n\nArtikulu berri bat argitaratu dugu ImationGroup-en blogean:\n\n"
        "{title}\n\n{excerpt}\n\nIrakurri artikulu osoa:\n{url}\n\n"
        "— ImationGroup\n\n──────────\n"
        "Ez duzu posta gehiago jaso nahi? Baja eman: {unsubscribe_url}",
    ),
    "et": (
        "{title} — ImationGroup",
        "Tere,\n\nAvaldasime uue artikli ImationGroup'i blogis:\n\n"
        "{title}\n\n{excerpt}\n\nLoe artiklit täies pikkuses:\n{url}\n\n"
        "— ImationGroup\n\n──────────\n"
        "Ei soovi enam kirju saada? Lõpeta tellimus: {unsubscribe_url}",
    ),
    "en": (
        "{title} — ImationGroup",
        "Hi,\n\nWe just published a new article on the ImationGroup blog:\n\n"
        "{title}\n\n{excerpt}\n\nRead the full post:\n{url}\n\n"
        "— ImationGroup\n\n──────────\n"
        "Don't want to receive more? Unsubscribe: {unsubscribe_url}",
    ),
}

# Small page rendered after confirm/unsubscribe -- minimal styling, no chrome
# import (newsletter pages live at a different mount than the blog).
PAGE_TEMPLATE = """<!doctype html>
<html lang="{lang}"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, follow">
<title>{title} — ImationGroup</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>body{{font-family:system-ui,sans-serif;max-width:520px;margin:10vh auto;padding:0 1.5rem;color:#1a1a2e;text-align:center;line-height:1.65}}
h1{{font-size:1.8rem;color:#0066CC;margin-bottom:.5rem}}p{{margin:.5rem 0;color:#5a606a}}a{{color:#0066CC}}
.icon{{font-size:3rem;color:#00A5A8;margin-bottom:1rem}}</style>
</head><body>
<div class="icon">{icon}</div>
<h1>{title}</h1>
<p>{body}</p>
<p style="margin-top:2rem"><a href="/{lang}/">← {home}</a></p>
</body></html>"""

I18N_PAGE_LABELS = {
    "confirmed":   {"es": ("Suscripción confirmada", "Ya estás dentro. Te enviaremos un email cada vez que publiquemos un artículo nuevo. Si en algún momento quieres darte de baja, cada email lleva su link."),
                    "gl": ("Subscrición confirmada", "Xa estás dentro. Enviarémosche un correo cada vez que publiquemos un artigo. Cada email leva o seu enlace de baixa."),
                    "ca": ("Subscripció confirmada", "Ja hi ets. T'enviarem un correu cada cop que publiquem un article. Cada email porta el seu enllaç per donar-te de baixa."),
                    "pt": ("Subscrição confirmada", "Estás dentro. Vamos enviar-te um email sempre que publicarmos um artigo. Cada email tem o link para te dares de baixa."),
                    "eu": ("Harpidetza berretsi da", "Bertan zaude. Artikulu berri bat argitaratzen dugun bakoitzean mezu bat bidaliko dizugu. Baja emateko esteka mezu bakoitzean dago."),
                    "et": ("Tellimus kinnitatud", "Oled tellijate hulgas. Saadame Sulle kirja iga uue artikli kohta. Iga kirja sees on tellimuse lõpetamise link."),
                    "en": ("Subscription confirmed", "You're in. We'll email you each time we publish a new article. Every email has its own unsubscribe link.")},
    "unsubscribed":{"es": ("Te has dado de baja", "Ya no recibirás más correos del boletín. Lamentamos verte ir; si cambias de idea, puedes volver a suscribirte cuando quieras."),
                    "gl": ("Dado de baixa", "Xa non recibirás máis correos. Se cambias de idea, podes volver subscribirte cando queiras."),
                    "ca": ("T'has donat de baixa", "Ja no rebràs més correus. Si canvies d'opinió, pots tornar a subscriure't quan vulguis."),
                    "pt": ("Cancelaste a subscrição", "Já não receberás mais emails. Se mudares de ideia, podes voltar a subscrever quando quiseres."),
                    "eu": ("Baja eman da", "Ez duzu mezu gehiago jasoko. Iritziz aldatuz gero, nahi duzunean berriz harpidetu zaitezke."),
                    "et": ("Tellimus lõpetatud", "Sa ei saa enam meilt kirju. Kui meelt muudad, võid alati uuesti tellida."),
                    "en": ("Unsubscribed", "You won't receive any more emails. If you change your mind, you can subscribe again any time.")},
    "invalid":     {"es": ("Enlace no válido", "El enlace que has usado no es válido o ha expirado."),
                    "gl": ("Enlace non válido", "O enlace usado non é válido ou caducou."),
                    "ca": ("Enllaç no vàlid", "L'enllaç que has fet servir no és vàlid o ha caducat."),
                    "pt": ("Link inválido", "O link que usaste não é válido ou expirou."),
                    "eu": ("Esteka baliogabea", "Erabili duzun esteka ez da baliozkoa edo iraungi da."),
                    "et": ("Vigane link", "Link, mida kasutasid, pole kehtiv või on aegunud."),
                    "en": ("Invalid link", "The link you used is not valid or has expired.")},
}
HOME_LABELS = {"es": "Volver al sitio", "gl": "Volver ao sitio", "ca": "Tornar al lloc",
               "pt": "Voltar ao site", "eu": "Itzuli", "et": "Tagasi", "en": "Back to home"}


# ── SMTP send: imports the contact backend's settings to avoid drift ───────
def _send_email(to: str, subject: str, body: str) -> bool:
    """Send via the same SMTP config the contact form uses."""
    from app.main import (
        SMTP_FROM, SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_USE_TLS, SMTP_USER,
    )
    import smtplib

    if not SMTP_HOST:
        log.warning("SMTP not configured; email NOT sent. to=%s subject=%r", to, subject)
        return False
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM
    msg["To"] = to
    msg.set_content(body)
    try:
        if SMTP_USE_TLS:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as s:
                s.starttls()
                if SMTP_USER: s.login(SMTP_USER, SMTP_PASSWORD)
                s.send_message(msg)
        else:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20) as s:
                if SMTP_USER: s.login(SMTP_USER, SMTP_PASSWORD)
                s.send_message(msg)
        return True
    except Exception:
        log.exception("error sending to %s", to)
        return False


def _tpl(map_: dict, lang: str) -> tuple[str, str]:
    return map_.get(lang) or map_[DEFAULT_LANG]


def _page(lang: str, kind: str) -> str:
    title, body = (I18N_PAGE_LABELS[kind].get(lang) or I18N_PAGE_LABELS[kind][DEFAULT_LANG])
    icon = {"confirmed": "✓", "unsubscribed": "✓", "invalid": "✗"}.get(kind, "")
    return PAGE_TEMPLATE.format(
        lang=lang, title=title, body=body, icon=icon,
        home=HOME_LABELS.get(lang, HOME_LABELS[DEFAULT_LANG]),
    )


# ── Naive in-process rate-limit (single uvicorn worker) ────────────────────
_RATE_WIN = 60 * 60
_RATE_MAX = 5
_BUCKETS: Dict[str, Deque[float]] = {}
_LOCK = Lock()


def _allow(ip: str) -> bool:
    now = time.time()
    with _LOCK:
        b = _BUCKETS.setdefault(ip, deque())
        while b and b[0] < now - _RATE_WIN: b.popleft()
        if len(b) >= _RATE_MAX: return False
        b.append(now); return True


def _client_ip(req: Request) -> str:
    fwd = req.headers.get("x-forwarded-for")
    return fwd.split(",")[0].strip() if fwd else (req.client.host if req.client else "?")


# ── Payload ────────────────────────────────────────────────────────────────
class SubscribePayload(BaseModel):
    email: EmailStr
    lang: Optional[str] = PField(default=None, max_length=4)
    website: Optional[str] = None  # honeypot


class SubscribeResponse(BaseModel):
    sent: bool


# ── Endpoints ──────────────────────────────────────────────────────────────
@router.post("/api/newsletter/subscribe", response_model=SubscribeResponse, include_in_schema=False)
def subscribe(payload: SubscribePayload, request: Request,
              bg: BackgroundTasks,
              session: Session = Depends(get_session)):
    ip = _client_ip(request)
    if payload.website:
        log.info("[newsletter] honeypot triggered ip=%s", ip)
        return SubscribeResponse(sent=True)  # silent ok to confuse bots

    if not _allow(ip):
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS,
                            "Demasiados intentos. Inténtalo más tarde.")

    email = payload.email.lower().strip()
    lang = (payload.lang or DEFAULT_LANG).lower()[:2]
    if lang not in LANGS:
        lang = DEFAULT_LANG

    existing = session.exec(select(Subscriber).where(Subscriber.email == email)).first()
    if existing and existing.status == "confirmed":
        # Already in — silent ok (don't reveal which addresses are subscribed).
        log.info("[newsletter] already confirmed: %s", email)
        return SubscribeResponse(sent=True)

    if existing:
        existing.lang = lang
        existing.status = "pending"
        existing.token = secrets.token_urlsafe(32)
        existing.unsubscribed_at = None
        sub = existing
    else:
        sub = Subscriber(
            email=email, lang=lang, status="pending",
            token=secrets.token_urlsafe(32),
        )
    session.add(sub); session.commit(); session.refresh(sub)

    # Send confirmation in background so the request returns instantly.
    bg.add_task(_send_confirm, sub.id)
    return SubscribeResponse(sent=True)


def _send_confirm(sub_id: int) -> None:
    with Session(engine) as s:
        sub = s.get(Subscriber, sub_id)
        if not sub: return
        subject, body = _tpl(CONFIRM_TEMPLATES, sub.lang)
        url = f"{SITE_URL}/newsletter/confirm/{sub.token}"
        _send_email(sub.email, subject, body.format(url=url))


@router.get("/newsletter/confirm/{token}", response_class=HTMLResponse, include_in_schema=False)
def confirm(token: str, session: Session = Depends(get_session)):
    sub = session.exec(select(Subscriber).where(Subscriber.token == token)).first()
    if not sub:
        return HTMLResponse(_page(DEFAULT_LANG, "invalid"), status_code=404)
    if sub.status != "confirmed":
        sub.status = "confirmed"
        sub.confirmed_at = datetime.now(timezone.utc)
        session.add(sub); session.commit()
    return HTMLResponse(_page(sub.lang, "confirmed"))


@router.get("/newsletter/unsubscribe/{token}", response_class=HTMLResponse, include_in_schema=False)
def unsubscribe(token: str, session: Session = Depends(get_session)):
    sub = session.exec(select(Subscriber).where(Subscriber.token == token)).first()
    if not sub:
        return HTMLResponse(_page(DEFAULT_LANG, "invalid"), status_code=404)
    if sub.status != "unsubscribed":
        sub.status = "unsubscribed"
        sub.unsubscribed_at = datetime.now(timezone.utc)
        session.add(sub); session.commit()
    return HTMLResponse(_page(sub.lang, "unsubscribed"))


# ── Fan-out helper: send a published post to all confirmed subscribers ─────
def send_post_to_subscribers(post_id: int) -> None:
    """Background task: email all confirmed subscribers of post.lang about
    this freshly published post. Idempotent-ish via last_sent_post_id so a
    publish→draft→publish loop doesn't spam (we send once per post per
    subscriber)."""
    with Session(engine) as s:
        post = s.get(Post, post_id)
        if not post or not post.is_published:
            return
        subs = s.exec(
            select(Subscriber).where(
                Subscriber.status == "confirmed",
                Subscriber.lang == post.lang,
            )
        ).all()
        log.info("[newsletter] post=%s lang=%s -> %d subscribers", post_id, post.lang, len(subs))

        subject_tpl, body_tpl = _tpl(NEWSLETTER_TEMPLATES, post.lang)
        url = f"{SITE_URL}/{post.lang}/blog/{post.slug}"
        excerpt = post.excerpt or _autoexcerpt(post.body_html or "")
        sent = 0
        for sub in subs:
            if sub.last_sent_post_id == post.id:
                continue  # already notified, skip
            subject = subject_tpl.format(title=post.title)
            body = body_tpl.format(
                title=post.title, excerpt=excerpt, url=url,
                unsubscribe_url=f"{SITE_URL}/newsletter/unsubscribe/{sub.token}",
            )
            if _send_email(sub.email, subject, body):
                sub.last_sent_post_id = post.id
                s.add(sub)
                sent += 1
        s.commit()
        log.info("[newsletter] post=%s sent=%d", post_id, sent)


_WS = re.compile(r"\s+")


def _autoexcerpt(html: str, n: int = 200) -> str:
    try:
        from bs4 import BeautifulSoup
        text = BeautifulSoup(html, "html.parser").get_text(separator=" ", strip=True)
    except ImportError:
        text = re.sub(r"<[^>]+>", " ", html)
    text = _WS.sub(" ", text).strip()
    return text if len(text) <= n else (text[:n].rsplit(" ", 1)[0] + "…")
