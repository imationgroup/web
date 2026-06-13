"""SQLite engine + dependency for FastAPI."""
from __future__ import annotations
from sqlmodel import SQLModel, create_engine, Session

from .config import DB_URL
from . import models  # noqa: F401  -- registers tables


engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
