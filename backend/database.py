"""SQLModel engine & session management.

Dev uses a local SQLite file (zero setup); the air-gapped enclave points
HELPDESK_DATABASE_URL at PostgreSQL + pgvector. Application code only
sees SQLModel sessions, so the switch is config-only.
"""
from __future__ import annotations

from sqlmodel import Session, SQLModel, create_engine

from backend.config import get_settings

_settings = get_settings()

_connect_args = {"check_same_thread": False} if _settings.database_url.startswith("sqlite") else {}
engine = create_engine(_settings.database_url, connect_args=_connect_args)


def init_db() -> None:
    # Import models so their tables are registered before create_all.
    from backend import models  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
