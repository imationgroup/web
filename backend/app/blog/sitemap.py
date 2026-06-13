"""Dynamic sitemap.xml — one document for the whole imationgroup.com site.

Combines static pages (5 templates × 7 langs), blog index pages (1 × 7),
and all published blog posts (each lang version of each post). hreflang
alternates per URL so Google clusters language variants. lastmod from
git for the static pages and from the post.updated_at column for posts.

Replaces the file-based sitemap the build script used to write. nginx
routes /sitemap.xml to this endpoint."""
from __future__ import annotations
import subprocess
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

from fastapi import APIRouter, Response
from sqlmodel import Session, select

from .config import DEFAULT_LANG, LANGS, SITE_URL
from .db import engine
from .models import Post

router = APIRouter(tags=["sitemap"])

# git history lives on the host repo, bind-mounted into the container at
# the same path so the default chrome.py works.
REPO = Path("/home/deploy/apps/imationgroup-web")

STATIC_PAGES = [
    # (slug, priority).  Empty slug means /<lang>/ (home).
    ("",          "1.0"),
    ("services",  "0.8"),
    ("projects",  "0.8"),
    ("terms",     "0.4"),
    ("privacy",   "0.4"),
]


def _abs(path: str) -> str:
    return SITE_URL + path


def _git_lastmod(*paths: str) -> str:
    """Most recent committer date across given paths, or today if git fails."""
    best = ""
    for p in paths:
        try:
            r = subprocess.run(
                ["git", "-C", str(REPO), "log", "-1", "--format=%cs", "--", p],
                capture_output=True, text=True, timeout=5,
            )
            d = (r.stdout or "").strip()
            if d and d > best:
                best = d
        except (FileNotFoundError, subprocess.SubprocessError):
            pass
    return best or date.today().isoformat()


def _url_block(loc: str, lastmod: str, priority: str,
               alternates: list[tuple[str, str]], default_url: str,
               changefreq: str = "monthly") -> str:
    alts = "\n".join(
        f'    <xhtml:link rel="alternate" hreflang="{l}" href="{escape(u)}" />'
        for l, u in alternates
    )
    xd = (
        f'    <xhtml:link rel="alternate" hreflang="x-default" '
        f'href="{escape(default_url)}" />'
    )
    return (
        "  <url>\n"
        f"    <loc>{escape(loc)}</loc>\n"
        f"    <lastmod>{lastmod}</lastmod>\n"
        f"    <changefreq>{changefreq}</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        f"{alts}\n{xd}\n"
        "  </url>"
    )


@router.get("/sitemap.xml", include_in_schema=False)
def sitemap() -> Response:
    blocks: list[str] = []

    # 1) Static pages (5 × 7 langs)
    for slug, priority in STATIC_PAGES:
        tpl_name = "index.html" if not slug else f"{slug}.html"
        lastmod = _git_lastmod(f"templates/{tpl_name}", "i18n.js")
        for lang in LANGS:
            url = _abs(f"/{lang}/{slug}" if slug else f"/{lang}/")
            alts = [(l, _abs(f"/{l}/{slug}" if slug else f"/{l}/")) for l in LANGS]
            default_url = _abs(f"/{DEFAULT_LANG}/{slug}" if slug else f"/{DEFAULT_LANG}/")
            blocks.append(_url_block(url, lastmod, priority, alts, default_url))

    # 2) Blog index pages (1 × 7 langs)
    today = date.today().isoformat()
    for lang in LANGS:
        url = _abs(f"/{lang}/blog/")
        alts = [(l, _abs(f"/{l}/blog/")) for l in LANGS]
        default_url = _abs(f"/{DEFAULT_LANG}/blog/")
        blocks.append(_url_block(url, today, "0.7", alts, default_url, changefreq="weekly"))

    # 3) Blog posts (one URL per published lang version, hreflang to siblings)
    with Session(engine) as session:
        posts = session.exec(
            select(Post).where(Post.is_published == True)  # noqa: E712
        ).all()
    by_group: dict[str, list[Post]] = {}
    for p in posts:
        by_group.setdefault(p.group_id, []).append(p)
    for siblings in by_group.values():
        sib_by_lang = {s.lang: s for s in siblings}
        for p in siblings:
            url = _abs(f"/{p.lang}/blog/{p.slug}")
            lastmod = (p.updated_at or p.published_at or p.created_at).date().isoformat()
            alts = [(l, _abs(f"/{l}/blog/{s.slug}")) for l, s in sib_by_lang.items()]
            # x-default points to the default-lang version if it exists,
            # otherwise to this URL.
            default_sib = sib_by_lang.get(DEFAULT_LANG) or p
            default_url = _abs(f"/{default_sib.lang}/blog/{default_sib.slug}")
            blocks.append(_url_block(url, lastmod, "0.6", alts, default_url, changefreq="monthly"))

    body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(blocks) + "\n"
        '</urlset>\n'
    )
    return Response(
        content=body,
        media_type="application/xml",
        headers={"Cache-Control": "public, max-age=3600"},  # 1 h CDN/browser cache
    )
