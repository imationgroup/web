"""Admin panel: login, list, create/edit, delete, translate, publish."""
from __future__ import annotations
import json
import logging
import secrets
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

log = logging.getLogger(__name__)

from .auth import (
    clear_cookie,
    current_admin,
    issue_cookie,
    require_admin,
    verify_password,
)
from .config import (
    ADMIN_USER,
    DEFAULT_LANG,
    LANG_NAMES,
    LANGS,
)
from .db import get_session
from .models import Category, Post, Subscriber
from .storage import make_slug, remove_uploaded, save_cover_image
from .translate import translate_post

router = APIRouter(prefix="/admin", tags=["blog-admin"])

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def _from_json(s):
    try:
        return json.loads(s or "{}")
    except (TypeError, json.JSONDecodeError):
        return {}


templates.env.filters["from_json"] = _from_json


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


# ───────────────────────── Login / logout ───────────────────────────────────

@router.get("/login", response_class=HTMLResponse, include_in_schema=False)
def login_form(request: Request, error: str = ""):
    if current_admin(request):
        return RedirectResponse("/admin/", status_code=303)
    return templates.TemplateResponse(
        "admin_login.html", {"request": request, "error": error}
    )


@router.post("/login", include_in_schema=False)
def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    if username.strip().lower() != ADMIN_USER or not verify_password(password):
        return templates.TemplateResponse(
            "admin_login.html",
            {"request": request, "error": "Invalid credentials"},
            status_code=401,
        )
    resp = RedirectResponse("/admin/", status_code=303)
    issue_cookie(resp, ADMIN_USER)
    return resp


@router.post("/logout", include_in_schema=False)
def logout():
    resp = RedirectResponse("/admin/login", status_code=303)
    clear_cookie(resp)
    return resp


# ───────────────────────── Dashboard / list ─────────────────────────────────

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def dashboard(
    request: Request,
    admin: str = Depends(require_admin),
    session: Session = Depends(get_session),
):
    # Group posts by group_id so the admin sees one row per article with its
    # available language versions.
    rows = session.exec(select(Post).order_by(Post.updated_at.desc())).all()
    by_group: dict = {}
    for p in rows:
        g = by_group.setdefault(p.group_id, {"langs": {}, "first": p})
        g["langs"][p.lang] = p
    groups = list(by_group.values())
    # Sort by most-recently-updated within each group
    groups.sort(key=lambda g: max(p.updated_at for p in g["langs"].values()), reverse=True)
    return templates.TemplateResponse(
        "admin_dashboard.html",
        {"request": request, "admin": admin, "groups": groups, "langs": LANGS,
         "lang_names": LANG_NAMES},
    )


# ───────────────────────── New / edit post ──────────────────────────────────

@router.get("/posts/new", response_class=HTMLResponse, include_in_schema=False)
def new_post_form(
    request: Request,
    admin: str = Depends(require_admin),
    session: Session = Depends(get_session),
):
    cats = session.exec(select(Category)).all()
    return templates.TemplateResponse(
        "admin_post_form.html",
        {
            "request": request, "admin": admin, "post": None,
            "categories": cats, "langs": LANGS, "lang_names": LANG_NAMES,
            "default_lang": DEFAULT_LANG, "siblings": [],
        },
    )


@router.get("/posts/{post_id}/edit", response_class=HTMLResponse, include_in_schema=False)
def edit_post_form(
    post_id: int,
    request: Request,
    admin: str = Depends(require_admin),
    session: Session = Depends(get_session),
):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(404)
    siblings = session.exec(
        select(Post).where(Post.group_id == post.group_id, Post.id != post.id)
    ).all()
    cats = session.exec(select(Category)).all()
    return templates.TemplateResponse(
        "admin_post_form.html",
        {
            "request": request, "admin": admin, "post": post,
            "categories": cats, "langs": LANGS, "lang_names": LANG_NAMES,
            "default_lang": DEFAULT_LANG, "siblings": siblings,
        },
    )


@router.post("/posts", include_in_schema=False)
def create_or_update_post(
    request: Request,
    bg: BackgroundTasks,
    admin: str = Depends(require_admin),
    session: Session = Depends(get_session),
    # Form fields
    post_id: Optional[int] = Form(None),
    group_id: Optional[str] = Form(None),
    lang: str = Form(...),
    title: str = Form(...),
    slug: str = Form(""),
    excerpt: str = Form(""),
    body_html: str = Form(""),
    category_id: str = Form(""),  # "" -> None
    is_published: Optional[str] = Form(None),
    source_lang: Optional[str] = Form(None),
    cover_image: UploadFile = File(None),
    remove_cover: Optional[str] = Form(None),
):
    if lang not in LANGS:
        raise HTTPException(400, f"unsupported lang {lang!r}")

    title = title.strip()
    if not title:
        raise HTTPException(400, "title required")

    safe_slug = make_slug(slug or title)

    # Ensure (lang, slug) uniqueness with a suffix if needed.
    base_slug = safe_slug
    suffix = 2
    existing_post = session.get(Post, post_id) if post_id else None
    while True:
        clash = session.exec(
            select(Post).where(Post.lang == lang, Post.slug == safe_slug)
        ).first()
        if not clash or (existing_post and clash.id == existing_post.id):
            break
        safe_slug = f"{base_slug}-{suffix}"
        suffix += 1

    cat_id = int(category_id) if category_id.strip().isdigit() else None
    publish = bool(is_published)

    notify_subscribers = False
    if existing_post:
        p = existing_post
        # If admin edited content, it's no longer "auto-translated".
        content_changed = (
            p.title != title
            or p.body_html != body_html
            or p.excerpt != excerpt.strip()
        )
        p.title = title
        p.slug = safe_slug
        p.excerpt = excerpt.strip()
        p.body_html = body_html
        p.category_id = cat_id
        p.lang = lang
        if content_changed:
            p.is_auto_translated = False
        was_published = p.is_published
        if publish and not p.is_published:
            p.published_at = _utcnow()
            notify_subscribers = True
        p.is_published = publish
        p.updated_at = _utcnow()
    else:
        gid = group_id or secrets.token_hex(16)
        p = Post(
            group_id=gid,
            lang=lang,
            slug=safe_slug,
            title=title,
            excerpt=excerpt.strip(),
            body_html=body_html,
            category_id=cat_id,
            is_published=publish,
            is_auto_translated=False,
            source_lang=source_lang or lang,
            published_at=_utcnow() if publish else None,
        )
        if publish:
            notify_subscribers = True

    # Cover image handling
    if remove_cover and p.cover_image:
        remove_uploaded(p.cover_image)
        p.cover_image = None
    if cover_image and cover_image.filename:
        try:
            new_path = save_cover_image(cover_image)
        except ValueError as e:
            raise HTTPException(400, str(e))
        if p.cover_image:
            remove_uploaded(p.cover_image)
        p.cover_image = new_path

    session.add(p)
    session.commit()
    session.refresh(p)

    # Sync the cover image across all language versions: it's the same
    # article, the hero image must be the same. Avoids the "es shows the
    # cover, en/gl/ca/... don't" bug when the admin uploads the image AFTER
    # translating.
    if p.cover_image is not None:
        for sib in session.exec(
            select(Post).where(Post.group_id == p.group_id, Post.id != p.id)
        ).all():
            if sib.cover_image != p.cover_image:
                sib.cover_image = p.cover_image
                session.add(sib)
        session.commit()

    # Fire newsletter fan-out when a post becomes published (transition only,
    # not on every save of an already-published post).
    if notify_subscribers:
        from .newsletter import send_post_to_subscribers
        bg.add_task(send_post_to_subscribers, p.id)

    return RedirectResponse(f"/admin/posts/{p.id}/edit", status_code=303)


@router.post("/posts/{post_id}/delete", include_in_schema=False)
def delete_post(
    post_id: int,
    admin: str = Depends(require_admin),
    session: Session = Depends(get_session),
):
    p = session.get(Post, post_id)
    if not p:
        raise HTTPException(404)
    if p.cover_image:
        remove_uploaded(p.cover_image)
    session.delete(p)
    session.commit()
    return RedirectResponse("/admin/", status_code=303)


def _snapshot(src: Post) -> dict:
    """Plain-dict copy of a Post's fields so a background worker doesn't
    share the request's Session."""
    return {
        "group_id": src.group_id, "lang": src.lang,
        "title": src.title, "excerpt": src.excerpt, "body_html": src.body_html,
        "cover_image": src.cover_image, "category_id": src.category_id,
        "source_lang": src.source_lang,
    }


@router.post("/posts/{post_id}/translate", include_in_schema=False)
def translate_to_all(
    post_id: int,
    bg: BackgroundTasks,
    admin: str = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Translate to EVERY other lang in parallel, in background."""
    src = session.get(Post, post_id)
    if not src:
        raise HTTPException(404)
    bg.add_task(_run_translations, post_id, _snapshot(src),
                [l for l in LANGS if l != src.lang])
    return RedirectResponse(
        f"/admin/posts/{post_id}/edit?translating=all", status_code=303
    )


@router.post("/posts/{post_id}/translate/{target_lang}", include_in_schema=False)
def translate_to_one(
    post_id: int,
    target_lang: str,
    bg: BackgroundTasks,
    admin: str = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Translate to ONE target lang. Same background pipeline, single-item list."""
    if target_lang not in LANGS:
        raise HTTPException(400, f"unsupported lang {target_lang!r}")
    src = session.get(Post, post_id)
    if not src:
        raise HTTPException(404)
    if target_lang == src.lang:
        raise HTTPException(400, "target lang same as source")
    bg.add_task(_run_translations, post_id, _snapshot(src), [target_lang])
    return RedirectResponse(
        f"/admin/posts/{post_id}/edit?translating={target_lang}", status_code=303
    )


def _run_translations(post_id: int, src: dict, targets: list[str]) -> None:
    """Fan out one Claude call per target language, in parallel. Writes to
    the DB happen on the same thread after all translations resolve, so
    SQLite stays single-writer."""
    from .db import engine

    log.info("[translate] post=%s source=%s -> targets=%s", post_id, src["lang"], targets)

    def one(target_lang: str):
        return target_lang, translate_post(
            source_lang=src["lang"],
            target_lang=target_lang,
            title=src["title"],
            excerpt=src["excerpt"],
            body_html=src["body_html"],
        )

    with ThreadPoolExecutor(max_workers=min(6, len(targets))) as pool:
        results = list(pool.map(one, targets))

    with Session(engine) as session:
        for target_lang, result in results:
            if not result:
                log.warning("[translate] post=%s target=%s: no result", post_id, target_lang)
                continue
            existing = session.exec(
                select(Post).where(Post.group_id == src["group_id"], Post.lang == target_lang)
            ).first()
            if existing and not existing.is_auto_translated:
                log.info("[translate] post=%s target=%s: skipped (hand-edited)", post_id, target_lang)
                continue
            if existing:
                existing.title = result["title"]
                existing.excerpt = result["excerpt"]
                existing.body_html = result["body_html"]
                existing.updated_at = _utcnow()
                existing.is_auto_translated = True
                existing.category_id = src["category_id"]
                existing.cover_image = src["cover_image"]
                session.add(existing)
            else:
                base = make_slug(result["title"])
                slug = base
                n = 2
                while session.exec(
                    select(Post).where(Post.lang == target_lang, Post.slug == slug)
                ).first():
                    slug = f"{base}-{n}"
                    n += 1
                session.add(
                    Post(
                        group_id=src["group_id"],
                        lang=target_lang,
                        slug=slug,
                        title=result["title"],
                        excerpt=result["excerpt"],
                        body_html=result["body_html"],
                        cover_image=src["cover_image"],
                        category_id=src["category_id"],
                        is_published=False,  # draft until admin reviews & publishes
                        is_auto_translated=True,
                        source_lang=src["source_lang"],
                    )
                )
        session.commit()
    log.info("[translate] post=%s done", post_id)


# ───────────────────────── Newsletter subscribers ──────────────────────────

@router.get("/subscribers", response_class=HTMLResponse, include_in_schema=False)
def subscribers_list(
    request: Request,
    admin: str = Depends(require_admin),
    session: Session = Depends(get_session),
):
    rows = session.exec(select(Subscriber).order_by(Subscriber.created_at.desc())).all()
    by_status: dict[str, int] = {"pending": 0, "confirmed": 0, "unsubscribed": 0}
    by_lang: dict[str, int] = {}
    for r in rows:
        by_status[r.status] = by_status.get(r.status, 0) + 1
        if r.status == "confirmed":
            by_lang[r.lang] = by_lang.get(r.lang, 0) + 1
    return templates.TemplateResponse(
        "admin_subscribers.html",
        {"request": request, "admin": admin, "rows": rows,
         "by_status": by_status, "by_lang": by_lang,
         "langs": LANGS, "lang_names": LANG_NAMES},
    )


@router.post("/subscribers/{sub_id}/delete", include_in_schema=False)
def delete_subscriber(
    sub_id: int,
    admin: str = Depends(require_admin),
    session: Session = Depends(get_session),
):
    s = session.get(Subscriber, sub_id)
    if s:
        session.delete(s)
        session.commit()
    return RedirectResponse("/admin/subscribers", status_code=303)


# ───────────────────────── Categories ───────────────────────────────────────

@router.get("/categories", response_class=HTMLResponse, include_in_schema=False)
def categories_list(
    request: Request,
    admin: str = Depends(require_admin),
    session: Session = Depends(get_session),
):
    cats = session.exec(select(Category)).all()
    items = []
    for c in cats:
        try:
            names = json.loads(c.names_json or "{}")
        except json.JSONDecodeError:
            names = {}
        items.append({"id": c.id, "slug": c.slug, "names": names})
    return templates.TemplateResponse(
        "admin_categories.html",
        {"request": request, "admin": admin, "items": items,
         "langs": LANGS, "lang_names": LANG_NAMES, "default_lang": DEFAULT_LANG},
    )


# ───────────────────────── Inline image upload ─────────────────────────────

@router.post("/upload", include_in_schema=False)
def upload_inline_image(
    file: UploadFile = File(...),
    admin: str = Depends(require_admin),
):
    """TinyMCE's images_upload_handler posts here when editor inserts an image.
    We reuse the same Pillow-resize-to-webp pipeline as the cover image.
    Returns JSON {"location": "/uploads/..."} per TinyMCE's expected shape."""
    try:
        public_path = save_cover_image(file)
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    return JSONResponse({"location": public_path})


# ───────────────────────── Draft preview ────────────────────────────────────

@router.get("/preview/{post_id}", response_class=HTMLResponse, include_in_schema=False)
def preview_post(
    post_id: int,
    request: Request,
    admin: str = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Render any post (draft or published) with the public template, plus a
    warning banner so the admin knows it's a preview. URL is admin-only."""
    from .routes_public import _render_preview
    return _render_preview(request, post_id, session)


@router.post("/categories", include_in_schema=False)
def create_or_update_category(
    request: Request,
    admin: str = Depends(require_admin),
    session: Session = Depends(get_session),
    category_id: Optional[int] = Form(None),
    slug: str = Form(...),
    name_default: str = Form(...),
):
    safe_slug = make_slug(slug or name_default)
    existing = session.get(Category, category_id) if category_id else None
    names = {DEFAULT_LANG: name_default.strip()}
    if existing:
        try:
            old = json.loads(existing.names_json or "{}")
            old.update(names)
            existing.names_json = json.dumps(old, ensure_ascii=False)
        except json.JSONDecodeError:
            existing.names_json = json.dumps(names, ensure_ascii=False)
        existing.slug = safe_slug
        session.add(existing)
    else:
        session.add(Category(slug=safe_slug, names_json=json.dumps(names, ensure_ascii=False)))
    session.commit()
    return RedirectResponse("/admin/categories", status_code=303)


@router.post("/categories/{cat_id}/delete", include_in_schema=False)
def delete_category(
    cat_id: int,
    admin: str = Depends(require_admin),
    session: Session = Depends(get_session),
):
    c = session.get(Category, cat_id)
    if c:
        session.delete(c)
        session.commit()
    return RedirectResponse("/admin/categories", status_code=303)
