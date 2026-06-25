"""Read the Claude-generated translations of templates/privacy.html and
templates/terms.html and inject them into i18n.js so the language
switcher actually changes the page content.

Reuses the same patch_lang helper pattern used by _gdpr_translate.py:
for each (lang, key, value) we either UPDATE the existing entry in
that language's dict or APPEND it at the end.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
I18N = ROOT / "i18n.js"
PRIVACY = ROOT / "privacy_translations.json"
TERMS = ROOT / "terms_translations.json"


def _js_string(s: str) -> str:
    """Encode a python str as a JS double-quoted string."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def patch_lang(src: str, lang: str, kv: dict[str, str]) -> tuple[str, int, int]:
    """Insert or update keys inside the `<lang>: { ... }` dict block."""
    pat = re.compile(rf"(\b{lang}\s*:\s*\{{)(.*?)(\}})", re.S)
    m = pat.search(src)
    if not m:
        print(f"  {lang}: NO MATCH"); return src, 0, 0
    inside = m.group(2)
    replaced = 0; added = 0
    for k, v in kv.items():
        repl = f"{k}:{_js_string(v)}"
        kpat = re.compile(rf'\b{k}\s*:\s*("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')')
        if kpat.search(inside):
            inside = kpat.sub(lambda _: repl, inside, count=1)
            replaced += 1
        else:
            inside = inside.rstrip().rstrip(",") + ",\n    " + repl
            added += 1
    return src[: m.start()] + m.group(1) + inside + m.group(3) + src[m.end():], replaced, added


def main():
    js = I18N.read_text(encoding="utf-8")
    for path in (PRIVACY, TERMS):
        bag = json.loads(path.read_text(encoding="utf-8"))
        print(f"=== {path.name} ===")
        for lang, kv in bag.items():
            js, rep, add = patch_lang(js, lang, kv)
            print(f"  {lang}: replaced={rep} added={add}")
    I18N.write_text(js, encoding="utf-8")
    print(f"\nwrote {I18N} ({len(js):,} bytes)")


if __name__ == "__main__":
    main()
