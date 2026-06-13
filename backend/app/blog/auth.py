"""Cookie-session auth for the single admin.

No DB users — credentials come from ADMIN_USER + ADMIN_PASSWORD_HASH in the
container env. The session is an itsdangerous-signed cookie containing only
the username (we re-verify the admin still matches on every request).
"""
from __future__ import annotations
import bcrypt
from fastapi import HTTPException, Request, status
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from .config import (
    ADMIN_PASSWORD_HASH,
    ADMIN_USER,
    SESSION_COOKIE,
    SESSION_MAX_AGE,
    SESSION_SECRET,
)


def _signer() -> URLSafeTimedSerializer:
    if not SESSION_SECRET:
        raise RuntimeError(
            "BLOG_SESSION_SECRET is empty. Set it in the container .env to a "
            "long random string (`python -c \"import secrets; print(secrets.token_urlsafe(48))\"`)."
        )
    return URLSafeTimedSerializer(SESSION_SECRET, salt="ig-admin-session")


def verify_password(plaintext: str) -> bool:
    if not ADMIN_PASSWORD_HASH:
        return False
    try:
        return bcrypt.checkpw(plaintext.encode("utf-8"), ADMIN_PASSWORD_HASH.encode("utf-8"))
    except ValueError:
        return False


def issue_cookie(response, username: str) -> None:
    token = _signer().dumps(username)
    response.set_cookie(
        SESSION_COOKIE,
        token,
        max_age=SESSION_MAX_AGE,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )


def clear_cookie(response) -> None:
    response.delete_cookie(SESSION_COOKIE, path="/")


def current_admin(request: Request) -> str:
    """Returns the admin username if session valid, else None."""
    raw = request.cookies.get(SESSION_COOKIE)
    if not raw or not ADMIN_USER:
        return None
    try:
        username = _signer().loads(raw, max_age=SESSION_MAX_AGE)
    except (BadSignature, SignatureExpired):
        return None
    if username != ADMIN_USER:
        return None
    return username


def require_admin(request: Request) -> str:
    """Dependency: 401 redirect-friendly response if no session."""
    admin = current_admin(request)
    if not admin:
        # 303 so the browser follows with GET, not whatever method we were on.
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/admin/login"},
        )
    return admin
