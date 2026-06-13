"""Translate posts via Claude. Preserves HTML structure; returns translated
title, excerpt and body. Falls back to a verbatim copy if no API key set
(admin can edit manually)."""
from __future__ import annotations
import json
import logging
from typing import Optional

from .config import ANTHROPIC_API_KEY, LANG_NAMES, TRANSLATION_MODEL

log = logging.getLogger(__name__)


def translate_post(
    *, source_lang: str, target_lang: str, title: str, excerpt: str, body_html: str
) -> Optional[dict]:
    """Return {"title", "excerpt", "body_html"} translated, or None on failure."""
    if not ANTHROPIC_API_KEY:
        log.warning("no ANTHROPIC_API_KEY: returning source as-is for %s->%s", source_lang, target_lang)
        return {"title": title, "excerpt": excerpt, "body_html": body_html}

    try:
        from anthropic import Anthropic
    except ImportError:
        log.exception("anthropic SDK not installed")
        return None

    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    src = LANG_NAMES.get(source_lang, source_lang)
    tgt = LANG_NAMES.get(target_lang, target_lang)
    system = (
        f"You translate blog posts from {src} to {tgt} for ImationGroup, a "
        "data-engineering and software consultancy. Preserve all HTML tags, "
        "attributes and structure exactly. Do not translate text inside <code> "
        "or <pre> blocks. Keep brand names like 'ImationGroup', 'AutoLinked', "
        "'AutoWhatsapp', 'AutoX' untranslated. Tone: professional, concise, "
        "trustworthy. Do not add commentary, only output the requested JSON."
    )
    user = (
        "Translate this blog post. Reply ONLY with a JSON object with keys "
        '"title", "excerpt" and "body_html". No markdown fence, no commentary.\n\n'
        f"<title>{title}</title>\n"
        f"<excerpt>{excerpt}</excerpt>\n"
        f"<body_html>{body_html}</body_html>"
    )

    try:
        resp = client.messages.create(
            model=TRANSLATION_MODEL,
            max_tokens=8192,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        text = resp.content[0].text.strip()
        # Defensive: strip a stray ```json fence if Claude adds one.
        if text.startswith("```"):
            text = text.strip("`")
            if text.startswith("json"):
                text = text[4:].strip()
        data = json.loads(text)
        return {
            "title": str(data.get("title", title)),
            "excerpt": str(data.get("excerpt", excerpt)),
            "body_html": str(data.get("body_html", body_html)),
        }
    except json.JSONDecodeError as e:
        log.warning("Claude returned non-JSON for %s->%s: %s", source_lang, target_lang, e)
        return None
    except Exception:
        log.exception("translation %s->%s failed", source_lang, target_lang)
        return None
