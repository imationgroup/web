"""Reuse the static site's chrome (navbar, footer, supporting CSS/JS) on
blog pages so they look identical to the rest of imationgroup.com.

At request time we read the per-language index.html the static build
produced, extract the bits that make the page look like the homepage,
and pass them to the blog templates. Cache per language; bust the
cache when index.html's mtime changes (so a static rebuild propagates
to the blog on the next request without a backend restart)."""
from __future__ import annotations
import os
import re
import threading
from pathlib import Path
from typing import NamedTuple, Optional

from bs4 import BeautifulSoup

# nginx root for the static site. Override in dev/tests via env var.
STATIC_ROOT = Path(os.getenv("STATIC_SITE_ROOT", "/home/deploy/apps/imationgroup-web"))


class Chrome(NamedTuple):
    head_style: str    # contents of the <style> block in <head> (without the tags)
    nav_html: str      # <nav class="navbar">...</nav>, ready to inject
    footer_html: str   # <footer class="footer">...</footer>, ready to inject
    scripts_html: str  # body <script> tags (lang switcher, dropdown, etc.) inlined


_CACHE: dict[str, tuple[float, Optional[Chrome]]] = {}
_LOCK = threading.Lock()


def chrome_for(lang: str) -> Optional[Chrome]:
    path = STATIC_ROOT / lang / "index.html"
    if not path.is_file():
        return None
    mtime = path.stat().st_mtime
    cached = _CACHE.get(lang)
    if cached and cached[0] == mtime:
        return cached[1]

    with _LOCK:
        # Re-check under lock to avoid duplicate parses.
        cached = _CACHE.get(lang)
        if cached and cached[0] == mtime:
            return cached[1]
        chrome = _extract(path, lang)
        _CACHE[lang] = (mtime, chrome)
        return chrome


def _rewrite_anchor_links(soup_root, lang: str) -> None:
    """In-page anchors like href="#home" are meaningless on a blog URL.
    Rewrite them to /<lang>/#home so they jump to the section on the
    homepage instead of scrolling to nowhere."""
    if soup_root is None:
        return
    for a in soup_root.find_all("a", href=True):
        href = a["href"]
        if href.startswith("#"):
            a["href"] = f"/{lang}/{href}"


def _extract(path: Path, lang: str) -> Chrome:
    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # Concatenate ALL <style> blocks in <head>. The static build emits at
    # least two: an @font-face block (added by inject_seo) and the main
    # template's big style block. find() returns only the first, dropping
    # all the actual UI rules.
    head = soup.head or soup
    head_style = "\n".join(s.decode_contents() for s in head.find_all("style"))

    nav = soup.find("nav", class_="navbar") or soup.find("nav")
    _rewrite_anchor_links(nav, lang)
    nav_html = str(nav) if nav else ""

    footer = soup.find("footer", class_="footer") or soup.find("footer")
    _rewrite_anchor_links(footer, lang)
    footer_html = str(footer) if footer else ""

    # Include body scripts so the lang switcher dropdown, mobile menu toggle,
    # smooth scroll, etc. all keep working. These are inlined in the static
    # build, no external src, so size is bounded and copying them is safe.
    scripts: list[str] = []
    body = soup.body
    if body:
        for s in body.find_all("script"):
            scripts.append(str(s))
    scripts_html = "\n".join(scripts)

    return Chrome(
        head_style=head_style,
        nav_html=nav_html,
        footer_html=footer_html,
        scripts_html=scripts_html,
    )
