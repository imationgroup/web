"""Blog config: paths, languages, environment-driven settings.

The blog shares the FastAPI process with the contact form. Data lives outside
the container under /var/imationgroup-blog so it survives image rebuilds.
"""
from __future__ import annotations
import os
from pathlib import Path

# Match the i18n languages of the main static site so the blog plays well
# with the existing hreflang/canonical structure.
LANGS = ["en", "es", "gl", "ca", "pt", "eu", "et"]
DEFAULT_LANG = "en"
LANG_NAMES = {
    "en": "English",  "es": "Español",  "gl": "Galego", "ca": "Català",
    "pt": "Português", "eu": "Euskera", "et": "Eesti",
}
FLAGS = {
    "en": "gb", "es": "es", "gl": "es-ga", "ca": "es-ct",
    "pt": "pt", "eu": "es-pv", "et": "ee",
}

# Storage. Docker-compose mounts /var/imationgroup-blog as a named volume.
DATA_ROOT = Path(os.getenv("BLOG_DATA_ROOT", "/var/imationgroup-blog"))
DB_PATH = DATA_ROOT / "db.sqlite3"
UPLOADS_DIR = DATA_ROOT / "uploads"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
DB_URL = f"sqlite:///{DB_PATH}"

# Cookie session for the admin.
SESSION_COOKIE = "ig_admin"
SESSION_MAX_AGE = 60 * 60 * 12  # 12 hours
SESSION_SECRET = os.getenv("BLOG_SESSION_SECRET", "")  # set in .env

# Auth — single admin, password as a bcrypt hash to avoid storing plaintext.
ADMIN_USER = os.getenv("ADMIN_USER", "").strip().lower()
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH", "").strip()

# Public URLs.
SITE_URL = os.getenv("SITE_URL", "https://imationgroup.com").rstrip("/")
PUBLIC_UPLOADS_PATH = "/uploads"  # nginx serves this from UPLOADS_DIR

# Translation. Falls back to no-op if no key (admin can edit manually).
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "").strip()
TRANSLATION_MODEL = os.getenv("BLOG_TRANSLATION_MODEL", "claude-haiku-4-5")

# Limits.
MAX_UPLOAD_BYTES = 8 * 1024 * 1024  # 8 MB
ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/webp", "image/gif"}
