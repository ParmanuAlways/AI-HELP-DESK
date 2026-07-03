"""Database models (SQLModel).

POC scope: just the Ticket table so voice-intake complaints persist and
the admin console can list them. The full schema (applications,
symptoms, dependencies, learning_examples…) lands with the seed script.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Ticket(SQLModel, table=True):
    __tablename__ = "tickets_poc"

    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_number: str = Field(index=True, unique=True)
    raw_text: str
    language: Optional[str] = None
    application: Optional[str] = None
    fault_type: Optional[str] = None
    severity: str = "medium"
    confidence: float = 0.0
    status: str = "pending_review"
    source: str = "voice"
    stub_stt: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
