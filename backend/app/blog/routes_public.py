"""Public-facing blog: /<lang>/blog/ index + /<lang>/blog/<slug> post.

Server-rendered HTML so the post content is in the initial HTML for crawlers.
Each post page emits canonical, hreflang to other published translations,
JSON-LD Article, OpenGraph and the matching <html lang>."""
from __future__ import annotations
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import quote_plus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from .chrome import chrome_for
from .config import DEFAULT_LANG, FLAGS, LANG_NAMES, LANGS, SITE_URL
from .db import get_session
from .models import Category, Post

router = APIRouter(prefix="/blog", tags=["blog-public"])

# Templates live alongside the package so the Dockerfile picks them up via
# COPY app ./app.
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ─── auto-excerpt: derive from body when the field is empty ─────────────────
try:
    from bs4 import BeautifulSoup as _BS
    _HAS_BS = True
except ImportError:
    _HAS_BS = False
_WS_RE = re.compile(r"\s+")


def _auto_excerpt(post, max_chars: int = 220) -> str:
    """Return post.excerpt if set, else first ~max_chars of plain text from
    body_html, cut at the nearest word boundary."""
    if post.excerpt:
        return post.excerpt
    body = post.body_html or ""
    if not body:
        return ""
    if _HAS_BS:
        text = _BS(body, "html.parser").get_text(separator=" ", strip=True)
    else:
        text = re.sub(r"<[^>]+>", " ", body)
    text = _WS_RE.sub(" ", text).strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "…"


def _urlencode(s: str) -> str:
    return quote_plus(s or "")


templates.env.filters["auto_excerpt"] = _auto_excerpt
templates.env.filters["urlenc"] = _urlencode


def _abs_url(path: str) -> str:
    return SITE_URL + path


def _lang_from_referer(req: Request) -> str:
    """Pick lang from URL path /<lang>/blog... or fall back to DEFAULT_LANG."""
    parts = req.url.path.lstrip("/").split("/")
    if parts and parts[0] in LANGS:
        return parts[0]
    return DEFAULT_LANG


def _categories_by_id(session: Session) -> dict:
    rows = session.exec(select(Category)).all()
    out = {}
    for c in rows:
        try:
            names = json.loads(c.names_json or "{}")
        except json.JSONDecodeError:
            names = {}
        out[c.id] = {"slug": c.slug, "names": names}
    return out


# Both /blog/ and /<lang>/blog/ are mapped here by main.py via the router prefix
# and an explicit /{lang}/blog mounting. We accept either form.
@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def blog_index_default(request: Request, session: Session = Depends(get_session)):
    return _render_index(request, DEFAULT_LANG, session)


@router.get("/{slug}", response_class=HTMLResponse, include_in_schema=False)
def blog_post_default(slug: str, request: Request, session: Session = Depends(get_session)):
    return _render_post(request, DEFAULT_LANG, slug, session)


def lang_router() -> APIRouter:
    r = APIRouter(tags=["blog-public"])

    @r.get("/{lang}/blog/", response_class=HTMLResponse, include_in_schema=False)
    def index(lang: str, request: Request, session: Session = Depends(get_session)):
        if lang not in LANGS:
            raise HTTPException(404)
        return _render_index(request, lang, session)

    @r.get("/{lang}/blog/{slug}", response_class=HTMLResponse, include_in_schema=False)
    def post(lang: str, slug: str, request: Request, session: Session = Depends(get_session)):
        if lang not in LANGS:
            raise HTTPException(404)
        return _render_post(request, lang, slug, session)

    return r


# Languages that fall back to Spanish in the blog index when no native
# translation exists. Pure UX call by the user: gl/ca/eu speakers also
# read Spanish, so showing them an es post is better than showing nothing.
# en/pt/et have no fallback -- those audiences are expected to want a
# proper native translation, so the post just doesn't appear there.
IBERIAN_FALLBACK_TO_ES = {"gl", "ca", "eu"}


def _render_index(request: Request, lang: str, session: Session) -> HTMLResponse:
    native = list(session.exec(
        select(Post)
        .where(Post.lang == lang, Post.is_published == True)  # noqa: E712
    ).all())

    fallback_posts: list[Post] = []
    if lang in IBERIAN_FALLBACK_TO_ES and lang != "es":
        native_group_ids = {p.group_id for p in native}
        es_posts = session.exec(
            select(Post)
            .where(Post.lang == "es", Post.is_published == True)  # noqa: E712
        ).all()
        fallback_posts = [p for p in es_posts if p.group_id not in native_group_ids]

    posts = sorted(
        native + fallback_posts,
        key=lambda p: p.published_at or p.created_at,
        reverse=True,
    )
    cats = _categories_by_id(session)
    return templates.TemplateResponse(
        "blog_index.html",
        {
            "request": request,
            "lang": lang,
            "langs": LANGS,
            "lang_names": LANG_NAMES,
            "flags": FLAGS,
            "default_lang": DEFAULT_LANG,
            "posts": posts,
            "categories": cats,
            "canonical": _abs_url(f"/{lang}/blog/"),
            "site_url": SITE_URL,
            "title": "Blog — ImationGroup",
            "chrome": chrome_for(lang) or chrome_for(DEFAULT_LANG),
            # Pass set of group_ids that are fallback (rendered with badge).
            "fallback_group_ids": {p.group_id for p in fallback_posts},
        },
    )


def _render_preview(request: Request, post_id: int, session: Session) -> HTMLResponse:
    """Render a post by id regardless of publish state. For admin preview."""
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(404)
    return _render_post_object(request, post, session, preview=True)


_BOT_UA_RE = re.compile(
    r"\b(bot|crawler|spider|slurp|crawl|preview|fetch|monitor|http_request|curl|wget|python|go-http|httpx|node-fetch|axios)\b",
    re.IGNORECASE,
)


def _looks_like_bot(request: Request) -> bool:
    ua = (request.headers.get("user-agent") or "").lower()
    return bool(_BOT_UA_RE.search(ua))


def _render_post(request: Request, lang: str, slug: str, session: Session) -> HTMLResponse:
    post = session.exec(
        select(Post).where(Post.lang == lang, Post.slug == slug, Post.is_published == True)  # noqa: E712
    ).first()
    if not post:
        raise HTTPException(404)
    # Count this view unless the request looks like a bot/crawler. Per-lang
    # post; the admin sees a per-translation breakdown plus a group total.
    if not _looks_like_bot(request):
        post.view_count = (post.view_count or 0) + 1
        session.add(post)
        session.commit()
        session.refresh(post)
    return _render_post_object(request, post, session, preview=False)


def _render_post_object(request: Request, post: "Post", session: Session, *, preview: bool) -> HTMLResponse:
    lang = post.lang
    # Find siblings (same group_id, other langs) for hreflang. In preview mode
    # include drafts too so the admin can navigate between language versions.
    q = select(Post).where(Post.group_id == post.group_id)
    if not preview:
        q = q.where(Post.is_published == True)  # noqa: E712
    siblings = session.exec(q).all()
    sibling_by_lang = {s.lang: s for s in siblings}

    cat = None
    if post.category_id:
        cats = _categories_by_id(session)
        cat = cats.get(post.category_id)

    canonical = _abs_url(f"/{lang}/blog/{post.slug}")
    image_abs = _abs_url(post.cover_image) if post.cover_image else _abs_url("/og-image.png")

    jsonld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.title,
        "description": post.excerpt or post.title,
        "image": image_abs,
        "inLanguage": lang,
        "datePublished": (post.published_at or post.created_at).isoformat(),
        "dateModified": post.updated_at.isoformat(),
        "url": canonical,
        "author": {"@type": "Organization", "name": "ImationGroup", "url": SITE_URL + "/"},
        "publisher": {
            "@type": "Organization",
            "name": "ImationGroup",
            "url": SITE_URL + "/",
            "logo": {"@type": "ImageObject", "url": _abs_url("/og-image.png")},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
    }

    return templates.TemplateResponse(
        "blog_post.html",
        {
            "request": request,
            "lang": lang,
            "langs": LANGS,
            "lang_names": LANG_NAMES,
            "flags": FLAGS,
            "default_lang": DEFAULT_LANG,
            "post": post,
            "category": cat,
            "sibling_by_lang": sibling_by_lang,
            "canonical": canonical,
            "image_abs": image_abs,
            "site_url": SITE_URL,
            "jsonld": json.dumps(jsonld, ensure_ascii=False, separators=(",", ":")),
            "preview": preview,
            "chrome": chrome_for(lang) or chrome_for(DEFAULT_LANG),
        },
    )
