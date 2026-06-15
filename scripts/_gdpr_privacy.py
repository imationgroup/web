"""One-off: update privacy.html so the cookies section is HONEST about
GA/GTM and so newsletter data is explicitly described. Replaces the
existing privacy_s7_* (Cookies) section and INSERTS a Newsletter section
before it. Updates 'Last updated' to today. Translations updated for
the 4 inline language dicts that exist in the template (en, es; gl/ca/
pt/eu/et fall through to English for the new keys -- explicit fallback
is fine for a legal text and we can translate later)."""
from __future__ import annotations
import re
from datetime import date
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "templates" / "privacy.html"
s = p.read_text(encoding="utf-8")

today = date.today().isoformat()

# 1. New HTML section for Newsletter (inserted before <h2 data-i18n="privacy_s7_title")
NEWSLETTER_SECTION = """
    <h2 data-i18n="privacy_sN_title">7. Newsletter Subscriptions</h2>
    <p data-i18n="privacy_sN_p1">When you subscribe to our newsletter from the website footer we collect and process:</p>
    <ul>
        <li data-i18n="privacy_sN_li1"><strong>Your email address</strong> — used only to send you new blog posts you opted in to receive.</li>
        <li data-i18n="privacy_sN_li2"><strong>Your language preference</strong> — so the newsletter and the confirmation email reach you in your language.</li>
        <li data-i18n="privacy_sN_li3"><strong>Subscription timestamps</strong> — proof of consent under GDPR (when you subscribed, when you confirmed, when/if you unsubscribed).</li>
    </ul>
    <p data-i18n="privacy_sN_p2"><strong>Legal basis:</strong> your explicit consent (GDPR Art. 6(1)(a)). The subscription uses double opt-in: you must click a confirmation link from your inbox before any newsletter is sent.</p>
    <p data-i18n="privacy_sN_p3"><strong>Withdrawal:</strong> every newsletter email contains a one-click unsubscribe link. You can also email <a href="mailto:info@imationgroup.com">info@imationgroup.com</a> to be removed.</p>
    <p data-i18n="privacy_sN_p4"><strong>Retention:</strong> we keep your subscription record while it is active. After you unsubscribe, we keep the email hash for 12 months solely to prevent accidental re-subscription, then erase it.</p>
"""

# 2. New honest Cookies section (replaces the old s7)
COOKIES_SECTION = """    <h2 data-i18n="privacy_s7_title">8. Cookies and Tracking</h2>
    <p data-i18n="privacy_s7_p1">We use two categories of cookies. You can change your choice any time using the "Cookie preferences" link in the footer.</p>
    <p data-i18n="privacy_s7_p2"><strong>Essential cookies</strong> — always loaded. These store your language choice and your cookie-banner decision in your browser's localStorage. No personal data, no tracking, no third party.</p>
    <p data-i18n="privacy_s7_p3"><strong>Analytics cookies</strong> — loaded ONLY after you click "Accept" on our cookie banner. We use Google Analytics 4 and Google Tag Manager (provider: Google Ireland Ltd.) with IP-anonymisation enabled. These cookies measure how the site is used so we can improve it. If you click "Reject", these scripts are never loaded and no Google cookies are placed.</p>
    <p data-i18n="privacy_s7_p4">A full list of Google's cookies and how to control them is available at <a href="https://policies.google.com/technologies/cookies" target="_blank" rel="noopener">policies.google.com/technologies/cookies</a>.</p>
"""

# Replace section 7 (existing) — drop everything from the `<h2 ... s7_title` to
# the next `<h2 ...` heading.
s = re.sub(
    r'    <h2 data-i18n="privacy_s7_title".*?(?=    <h2 data-i18n="privacy_s8_title")',
    NEWSLETTER_SECTION + "\n" + COOKIES_SECTION + "\n",
    s, count=1, flags=re.S,
)

# 3. Update "Last updated" date in all inline language dicts.
s = re.sub(
    r'(privacy_updated:\s*)"Last updated:[^"]*"',
    rf'\1"Last updated: {today}"',
    s,
)
s = re.sub(
    r'(privacy_updated:\s*)"Última actualización:[^"]*"',
    rf'\1"Última actualización: {today}"',
    s,
)
s = re.sub(
    r'(privacy_updated:\s*)"Última actualización:[^"]*"',
    rf'\1"Última actualización: {today}"',
    s,
)

# 4. Replace the falsified s7 text in every lang dict (en/es/gl/ca/pt/eu/et).
#    We replace the FIRST occurrence of `privacy_s7_p1: "..."` with the new
#    accurate text (en) and add the new accurate keys.
def patch_lang_dict(s: str, lang_code: str, replacements: dict) -> str:
    """Inside `<lang>: { ... }`, override or add keys."""
    pat = re.compile(rf'(\b{lang_code}\s*:\s*\{{)(.*?)(\}})', re.S)
    m = pat.search(s)
    if not m:
        return s
    inside = m.group(2)
    for key, val in replacements.items():
        # Escape val for use in regex replacement
        repl = key + ': ' + repr(val).replace("\\", "\\\\")
        # Replace existing key if present, else append
        if re.search(rf'\b{key}\s*:\s*"', inside):
            inside = re.sub(rf'\b{key}\s*:\s*"[^"]*"', repl, inside, count=1)
        else:
            inside = inside.rstrip().rstrip(',') + ',\n        ' + repl
    return s[:m.start()] + m.group(1) + inside + m.group(3) + s[m.end():]


EN = {
    "privacy_s1_li1": "Contact Information: Name, email address and message you provide via the contact form. Your IP address is logged briefly for spam protection.",
    "privacy_sN_title": "7. Newsletter Subscriptions",
    "privacy_sN_p1": "When you subscribe to our newsletter from the website footer we collect and process:",
    "privacy_sN_li1": "Your email address — used only to send you new blog posts you opted in to receive.",
    "privacy_sN_li2": "Your language preference — so the newsletter and the confirmation email reach you in your language.",
    "privacy_sN_li3": "Subscription timestamps — proof of consent under GDPR (when you subscribed, when you confirmed, when/if you unsubscribed).",
    "privacy_sN_p2": "Legal basis: your explicit consent (GDPR Art. 6(1)(a)). The subscription uses double opt-in: you must click a confirmation link from your inbox before any newsletter is sent.",
    "privacy_sN_p3": "Withdrawal: every newsletter email contains a one-click unsubscribe link. You can also email info@imationgroup.com to be removed.",
    "privacy_sN_p4": "Retention: we keep your subscription record while it is active. After you unsubscribe, we keep the email hash for 12 months solely to prevent accidental re-subscription, then erase it.",
    "privacy_s7_title": "8. Cookies and Tracking",
    "privacy_s7_p1": "We use two categories of cookies. You can change your choice any time using the 'Cookie preferences' link in the footer.",
    "privacy_s7_p2": "Essential cookies — always loaded. These store your language choice and your cookie-banner decision in your browser's localStorage. No personal data, no tracking, no third party.",
    "privacy_s7_p3": "Analytics cookies — loaded ONLY after you click 'Accept' on our cookie banner. We use Google Analytics 4 and Google Tag Manager (provider: Google Ireland Ltd.) with IP-anonymisation enabled. These cookies measure how the site is used so we can improve it. If you click 'Reject', these scripts are never loaded and no Google cookies are placed.",
    "privacy_s7_p4": "A full list of Google's cookies and how to control them is available at policies.google.com/technologies/cookies.",
}
ES = {
    "privacy_s1_li1": "Información de contacto: nombre, email y mensaje que aportas a través del formulario. Tu IP se registra brevemente para prevenir spam.",
    "privacy_sN_title": "7. Suscripciones al boletín",
    "privacy_sN_p1": "Cuando te suscribes al boletín desde el pie del sitio recogemos y tratamos:",
    "privacy_sN_li1": "Tu dirección de email — solo para enviarte los nuevos artículos del blog a los que has optado por suscribirte.",
    "privacy_sN_li2": "Tu preferencia de idioma — para que el boletín y el correo de confirmación te lleguen en tu lengua.",
    "privacy_sN_li3": "Marcas de tiempo de la suscripción — prueba del consentimiento según el RGPD (cuándo te suscribiste, cuándo confirmaste, cuándo te diste de baja si lo hiciste).",
    "privacy_sN_p2": "Base jurídica: tu consentimiento explícito (Art. 6(1)(a) RGPD). La suscripción usa doble opt-in: tienes que hacer click en un enlace de confirmación enviado a tu bandeja antes de que se envíe ningún correo.",
    "privacy_sN_p3": "Retirada del consentimiento: cada boletín incluye un enlace de baja con un solo click. También puedes escribir a info@imationgroup.com para que te eliminemos.",
    "privacy_sN_p4": "Conservación: guardamos tu registro de suscripción mientras está activa. Tras darte de baja, conservamos el hash de tu email durante 12 meses con el único fin de evitar re-suscripciones accidentales; pasado ese plazo se borra.",
    "privacy_s7_title": "8. Cookies y seguimiento",
    "privacy_s7_p1": "Usamos dos categorías de cookies. Puedes cambiar tu elección en cualquier momento mediante el enlace 'Preferencias de cookies' del pie.",
    "privacy_s7_p2": "Cookies esenciales — siempre cargadas. Guardan tu elección de idioma y tu decisión sobre el banner de cookies en el localStorage del navegador. No contienen datos personales, no rastrean y no son de terceros.",
    "privacy_s7_p3": "Cookies de analítica — se cargan SOLO si pulsas 'Aceptar' en el banner de cookies. Usamos Google Analytics 4 y Google Tag Manager (proveedor: Google Ireland Ltd.) con anonimización de IP activada. Estas cookies miden cómo se usa el sitio para que podamos mejorarlo. Si pulsas 'Rechazar', estos scripts nunca se cargan y no se deposita ninguna cookie de Google.",
    "privacy_s7_p4": "El listado completo de cookies de Google y cómo controlarlas está en policies.google.com/technologies/cookies.",
}

s = patch_lang_dict(s, "en", EN)
s = patch_lang_dict(s, "es", ES)

p.write_text(s, encoding="utf-8")
print("privacy.html updated.")
