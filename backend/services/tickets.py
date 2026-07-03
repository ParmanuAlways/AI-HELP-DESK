"""Ticket intake service.

POC-level: turns a raw complaint (from voice or text) into a persisted
ticket. Classification here is a lightweight keyword pass — a placeholder
for the real embed → pgvector search → LLM/agent pipeline described in
docs/agentic_workflows.md. Kept behind this seam so the voice layer never
needs to change when the real classifier lands.
"""
from __future__ import annotations

from sqlmodel import Session

from backend.database import engine
from backend.models import Ticket
from backend.schemas import Classification

# Minimal keyword hints just so the POC returns something meaningful.
# Replaced later by embeddings + LLM classification.
_APP_HINTS = {
    "eoffice": "eOffice",
    "e-office": "eOffice",
    "i-key": "eOffice",
    "ikey": "eOffice",
    "cabinet": "eOffice",
}
_FAULT_HINTS = {
    "login": "login / authentication",
    "i-key": "login / authentication",
    "ikey": "login / authentication",
    "sign": "signing failure",
    "upload": "document upload failure",
    "slow": "performance / slowness",
    "sluggish": "performance / slowness",
    "not found": "file-not-found",
    "delete": "data loss",
}


def classify(text: str) -> Classification:
    low = text.lower()
    app = next((v for k, v in _APP_HINTS.items() if k in low), None)
    fault = next((v for k, v in _FAULT_HINTS.items() if k in low), None)
    hits = sum(1 for k in _FAULT_HINTS if k in low)
    confidence = min(0.3 + 0.2 * hits, 0.9) if fault else 0.1
    return Classification(
        application=app,
        fault_type=fault,
        severity="medium",
        confidence=round(confidence, 2),
        reasoning="POC keyword stub — real embed+LLM classification pending.",
    )


def create_ticket(
    raw_text: str,
    classification: Classification,
    language: str | None = None,
    source: str = "voice",
    stub_stt: bool = False,
) -> Ticket:
    """Persist a provisional ticket and assign its number from the DB id."""
    with Session(engine) as session:
        ticket = Ticket(
            ticket_number="PENDING",
            raw_text=raw_text,
            language=language,
            application=classification.application,
            fault_type=classification.fault_type,
            severity=classification.severity,
            confidence=classification.confidence,
            status="pending_review",
            source=source,
            stub_stt=stub_stt,
        )
        session.add(ticket)
        session.flush()  # allocate id
        ticket.ticket_number = f"TKT-{ticket.id:05d}"
        session.commit()
        session.refresh(ticket)
        return ticket
