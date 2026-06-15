"""Rename footer columns 'Company' -> 'Enlaces' (Links) and 'Support' -> 'Legal'
in all 7 langs. Also drop the 'unsubscribe any time' tail from the newsletter
subtitle (already mentioned right below in the privacy line)."""
import re
from pathlib import Path

KEYS = {
    "en": {
        "footer_company": "Links",
        "footer_support": "Legal",
        "newsletter_subtitle": "New posts in your inbox.",
    },
    "es": {
        "footer_company": "Enlaces",
        "footer_support": "Legal",
        "newsletter_subtitle": "Nuevos artículos en tu buzón.",
    },
    "gl": {
        "footer_company": "Enlaces",
        "footer_support": "Legal",
        "newsletter_subtitle": "Novos artigos no teu buzón.",
    },
    "ca": {
        "footer_company": "Enllaços",
        "footer_support": "Legal",
        "newsletter_subtitle": "Nous articles a la teva safata.",
    },
    "pt": {
        "footer_company": "Ligações",
        "footer_support": "Legal",
        "newsletter_subtitle": "Novos artigos na tua caixa.",
    },
    "eu": {
        "footer_company": "Estekak",
        "footer_support": "Legala",
        "newsletter_subtitle": "Artikulu berriak zure postontzira.",
    },
    "et": {
        "footer_company": "Lingid",
        "footer_support": "Õigusteave",
        "newsletter_subtitle": "Uued postitused otse postkasti.",
    },
}


def _js(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def patch_lang(s: str, lang: str, kv: dict) -> str:
    pat = re.compile(rf'(\b{lang}\s*:\s*\{{)(.*?)(\}})', re.S)
    m = pat.search(s)
    if not m:
        print(f"  {lang}: NO MATCH"); return s
    inside = m.group(2); rep = add = 0
    for k, v in kv.items():
        repl = f"{k}:{_js(v)}"
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
