"""Ticket intake service.

POC-level stub: turns a raw complaint (from voice or text) into a
provisional ticket. Classification here is a lightweight keyword pass —
a placeholder for the real embed → pgvector search → LLM/agent pipeline
described in docs/agentic_workflows.md. Kept behind this seam so the
voice layer never needs to change when the real classifier lands.
"""
from __future__ import annotations

import itertools

from backend.schemas import Classification

_counter = itertools.count(1)

# Minimal keyword hints just so the POC returns something meaningful.
# Replaced later by embeddings + LLM classification.
_APP_HINTS = {
    "eoffice": "eOffice",
    "i-key": "eOffice",
    "ikey": "eOffice",
    "cabinet": "eOffice",
    "login": None,  # ambiguous across apps
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
    app = next((v for k, v in _APP_HINTS.items() if v and k in low), None)
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


def next_ticket_number() -> str:
    # Enclave will use a DB sequence; POC uses an in-process counter.
    return f"TKT-{next(_counter):05d}"
