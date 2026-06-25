"""Translate every data-i18n key in templates/privacy.html (and
templates/terms.html) into es/gl/ca/pt/eu/et using Claude, then patch
i18n.js so the language switcher actually changes the page content.

Designed to be run on the VPS inside the autolinked-saas backend
container which already has the anthropic SDK installed and the
ANTHROPIC_API_KEY env var. From the repo root:

    python3 _privacy_translate_local.py

The script needs three arguments via env:

    EXTRACT_FROM   path to the source template (defaults to /work/templates/privacy.html)
    OUT_JSON       path to write the translations dict (so the local
                   patch step can read it without internet)
"""
import json
import os
import re
import sys

from anthropic import Anthropic

LANGS = ["es", "gl", "ca", "pt", "eu", "et"]
LANG_NAMES = {
    "es": "Spanish (Spain, formal usted form)",
    "gl": "Galician",
    "ca": "Catalan",
    "pt": "Portuguese (Portugal)",
    "eu": "Basque (Euskara)",
    "et": "Estonian",
}

EXTRACT_FROM = os.environ.get("EXTRACT_FROM", "/work/templates/privacy.html")
OUT_JSON = os.environ.get("OUT_JSON", "/work/translations.json")
MODEL = os.environ.get("TRANSLATION_MODEL", "claude-haiku-4-5-20251001")

src = open(EXTRACT_FROM, encoding="utf-8").read()

# Pull data-i18n="<key>">text</tag — text-only elements (matches build-i18n.py's
# TAG_RE pattern). Same regex as build-i18n.py so we cover the same keys.
TAG_RE = re.compile(r'<(\w+)([^>]*?)\sdata-i18n="([^"]+)"([^>]*)>([^<]*)</\1>', re.S)
TITLE_RE = re.compile(r'<title([^>]*?)\sdata-i18n="([^"]+)"([^>]*)>([^<]*)</title>', re.S)

keys = {}
for m in TAG_RE.finditer(src):
    key, default = m.group(3), m.group(5).strip()
    if default:
        keys[key] = default
for m in TITLE_RE.finditer(src):
    key, default = m.group(2), m.group(4).strip()
    if default:
        keys[key] = default

print(f"extracted {len(keys)} keys from {EXTRACT_FROM}", file=sys.stderr)

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

out: dict[str, dict[str, str]] = {}
for lang in LANGS:
    print(f"  translating -> {lang}", file=sys.stderr)
    system = (
        "You translate UI strings for ImationGroup, a software development "
        "and data engineering consultancy. Output ONLY a JSON object whose "
        "keys are exactly the input keys and whose values are the translated "
        "strings. Preserve punctuation and line breaks. Do not translate "
        "brand names (ImationGroup, AutoLinked, AutoWhatsapp, AutoX, GDPR, "
        "RGPD). Do not add any commentary or markdown fences. Tone: "
        "professional, concise, trustworthy."
    )
    user = (
        f"Translate the following English strings to {LANG_NAMES[lang]}. "
        "Reply with ONLY the JSON object — no markdown fence, no commentary.\n\n"
        + json.dumps(keys, ensure_ascii=False, indent=2)
    )
    resp = client.messages.create(
        model=MODEL,
        max_tokens=8000,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    text = resp.content[0].text.strip()
    # Strip ``` fences if Claude adds them anyway
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    try:
        d = json.loads(text)
    except Exception as e:
        print(f"  {lang}: FAILED to parse — {e}\n  raw[:400]={text[:400]}", file=sys.stderr)
        continue
    out[lang] = d
    print(f"    got {len(d)} keys", file=sys.stderr)

with open(OUT_JSON, "w", encoding="utf-8") as fp:
    json.dump(out, fp, ensure_ascii=False, indent=2)
print(f"wrote {OUT_JSON}", file=sys.stderr)
