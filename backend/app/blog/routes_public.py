"""Public-facing blog: /<lang>/blog/ index + /<lang>/blog/<slug> post.

Server-rendered HTML so the post content is in the initial HTML for crawlers.
Each post page emits canonical, hreflang to other published translations,
JSON-LD Article, OpenGraph and the matching <html lang>."""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from .config import DEFAULT_LANG, FLAGS, LANG_NAMES, LANGS, SITE_URL
from .db import get_session
from .models import Category, Post

router = APIRouter(prefix="/blog", tags=["blog-public"])

# Templates live alongside the package so the Dockerfile picks them up via
# COPY app ./app.
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


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


def _render_index(request: Request, lang: str, session: Session) -> HTMLResponse:
    posts = session.exec(
        select(Post)
        .where(Post.lang == lang, Post.is_published == True)  # noqa: E712
        .order_by(Post.published_at.desc().nulls_last())
    ).all()
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
        },
    )


def _render_post(request: Request, lang: str, slug: str, session: Session) -> HTMLResponse:
    post = session.exec(
        select(Post).where(Post.lang == lang, Post.slug == slug, Post.is_published == True)  # noqa: E712
    ).first()
    if not post:
        raise HTTPException(404)

    # Find published siblings (same group_id, other langs) for hreflang.
    siblings = session.exec(
        select(Post).where(Post.group_id == post.group_id, Post.is_published == True)  # noqa: E712
    ).all()
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
        },
    )
