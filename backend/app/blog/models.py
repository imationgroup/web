"""SQLModel tables for the blog: Category and Post.

Multilingual model: a 'Post' row is ONE language. All translations of the
same post share `group_id` (UUID). The admin picks a source language, then
can trigger auto-translation which materialises the other 6 rows.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(unique=True, index=True, max_length=80)
    # JSON: {"en": "Engineering", "es": "Ingeniería", ...}
    # Stored as TEXT; UI manages it as a dict.
    names_json: str = Field(default="{}")
    created_at: datetime = Field(default_factory=utcnow)


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Groups all language versions of the same post.
    group_id: str = Field(index=True, max_length=36)
    lang: str = Field(index=True, max_length=4)
    # Slug is per (lang, lang-version). Composite unique enforced at app
    # level + an index for fast URL lookup.
    slug: str = Field(index=True, max_length=160)
    title: str = Field(max_length=240)
    excerpt: str = Field(default="", max_length=480)
    body_html: str = ""  # rich-text from TinyMCE
    cover_image: Optional[str] = None  # path like "/uploads/2026/06/abc.jpg"
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    is_published: bool = Field(default=False, index=True)
    # True if this row came from Claude and has NOT been hand-edited since.
    is_auto_translated: bool = Field(default=False)
    source_lang: str = Field(max_length=4)  # the lang it was originally written in
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    published_at: Optional[datetime] = None
