"""Add newsletter form labels to all 7 languages in i18n.js so 'Newsletter'
doesn't leak through as English on non-EN pages. ES gets 'Boletín' per the
user's explicit request."""
import re
from pathlib import Path

KEYS = {
    "en": {
        "newsletter_title": "Newsletter",
        "newsletter_subtitle": "New posts in your inbox. Unsubscribe any time.",
        "newsletter_email_placeholder": "you@example.com",
        "newsletter_subscribe": "Subscribe",
    },
    "es": {
        "newsletter_title": "Boletín",
        "newsletter_subtitle": "Nuevos artículos en tu buzón. Baja en cualquier momento.",
        "newsletter_email_placeholder": "tu@email.com",
        "newsletter_subscribe": "Suscribirme",
    },
    "gl": {
        "newsletter_title": "Boletín",
        "newsletter_subtitle": "Novos artigos no teu buzón. Baixa en calquera momento.",
        "newsletter_email_placeholder": "ti@email.com",
        "newsletter_subscribe": "Subscribirme",
    },
    "ca": {
        "newsletter_title": "Butlletí",
        "newsletter_subtitle": "Nous articles a la teva safata. Baixa quan vulguis.",
        "newsletter_email_placeholder": "tu@correu.com",
        "newsletter_subscribe": "Subscriu-me",
    },
    "pt": {
        "newsletter_title": "Newsletter",
        "newsletter_subtitle": "Novos artigos na tua caixa. Cancela quando quiseres.",
        "newsletter_email_placeholder": "tu@email.com",
        "newsletter_subscribe": "Subscrever",
    },
    "eu": {
        "newsletter_title": "Buletina",
        "newsletter_subtitle": "Artikulu berriak zure postontzira. Baja edozein unetan.",
        "newsletter_email_placeholder": "zu@email.com",
        "newsletter_subscribe": "Harpidetu",
    },
    "et": {
        "newsletter_title": "Uudiskiri",
        "newsletter_subtitle": "Uued postitused otse postkasti. Lopeta millal soovid.",
        "newsletter_email_placeholder": "sina@email.com",
        "newsletter_subscribe": "Telli",
    },
}


def _js_string(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def patch_lang(s: str, lang: str, kv: dict) -> str:
    pat = re.compile(rf'(\b{lang}\s*:\s*\{{)(.*?)(\}})', re.S)
    m = pat.search(s)
    if not m:
        print(f"  {lang}: NO MATCH"); return s
    inside = m.group(2)
    rep = 0; add = 0
    for k, v in kv.items():
        repl = f"{k}:{_js_string(v)}"
        kpat = re.compile(rf'\b{k}\s*:\s*("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')')
        if kpat.search(inside):
            inside = kpat.sub(lambda _: repl, inside, count=1); rep += 1
        else:
            inside = inside.rstrip().rstrip(",") + ",\n    " + repl; add += 1
    print(f"  {lang}: replaced={rep} added={add}")
    return s[: m.start()] + m.group(1) + inside + m.group(3) + s[m.end():]


p = Path(__file__).resolve().parent.parent / "i18n.js"
s = p.read_text(encoding="utf-8")
for lang, kv in KEYS.items():
    s = patch_lang(s, lang, kv)
p.write_text(s, encoding="utf-8")
print("Done.")
