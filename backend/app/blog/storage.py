"""Image upload + resize + slug helpers."""
from __future__ import annotations
import io
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import UploadFile
from PIL import Image
from slugify import slugify

from .config import (
    ALLOWED_IMAGE_TYPES,
    MAX_UPLOAD_BYTES,
    PUBLIC_UPLOADS_PATH,
    UPLOADS_DIR,
)


def make_slug(text: str) -> str:
    """Lowercase, ascii, hyphenated. Empty input -> 'post'."""
    s = slugify(text or "", lowercase=True, max_length=100)
    return s or "post"


def save_cover_image(upload: UploadFile) -> str:
    """Validate, downscale, write under uploads/, return /uploads/<rel> URL."""
    if upload.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError(f"image type {upload.content_type!r} not allowed")

    raw = upload.file.read(MAX_UPLOAD_BYTES + 1)
    if len(raw) > MAX_UPLOAD_BYTES:
        raise ValueError(f"image larger than {MAX_UPLOAD_BYTES//1024//1024} MB")
    if not raw:
        raise ValueError("empty upload")

    try:
        img = Image.open(io.BytesIO(raw))
        img.load()
    except Exception as e:
        raise ValueError(f"not a valid image: {e}")

    # Downscale to a reasonable max width; keep aspect ratio.
    MAX_W = 1600
    if img.width > MAX_W:
        ratio = MAX_W / img.width
        img = img.resize((MAX_W, int(img.height * ratio)), Image.LANCZOS)

    # Re-encode to WebP for smaller payload + consistent format.
    today = datetime.now(timezone.utc)
    rel_dir = f"{today.year}/{today.month:02d}"
    out_dir = UPLOADS_DIR / rel_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    name = f"{secrets.token_hex(8)}.webp"
    out_path = out_dir / name

    if img.mode in ("RGBA", "P", "LA"):
        img = img.convert("RGB")  # WebP supports RGBA too but JPEG-bg is cleaner for covers
    img.save(out_path, format="WEBP", quality=82, method=4)

    return f"{PUBLIC_UPLOADS_PATH}/{rel_dir}/{name}"


def remove_uploaded(public_path: Optional[str]) -> None:
    """Best-effort delete an uploaded asset given its /uploads/... path."""
    if not public_path or not public_path.startswith(PUBLIC_UPLOADS_PATH + "/"):
        return
    rel = public_path[len(PUBLIC_UPLOADS_PATH) + 1:]
    abs_path = UPLOADS_DIR / rel
    try:
        if abs_path.is_file():
            abs_path.unlink()
    except OSError:
        pass
