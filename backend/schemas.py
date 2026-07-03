"""Pydantic request/response schemas for the API."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Classification(BaseModel):
    """AI classification result for a complaint (stubbed for the POC)."""

    application: Optional[str] = None
    fault_type: Optional[str] = None
    severity: str = "medium"
    confidence: float = 0.0
    reasoning: Optional[str] = None


class TranscriptResult(BaseModel):
    """What we send back to the browser after a voice call ends."""

    session_id: str
    transcript: str
    language: Optional[str] = None
    duration_sec: Optional[float] = None
    stub: bool = False


class VoiceTicketResult(BaseModel):
    """Final result of a voice intake: transcript + provisional ticket.

    In the POC the operator reviews the transcript and classification
    before the ticket is finalised (human-in-the-loop).
    """

    session_id: str
    transcript: str
    language: Optional[str] = None
    classification: Classification
    ticket_number: str
    status: str = "pending_review"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    stub_stt: bool = False
