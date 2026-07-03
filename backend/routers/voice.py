"""Voice intake router — WebRTC (browser) → WebSocket → STT → ticket.

POC transport: the browser captures the mic via getUserMedia + the
MediaRecorder API and streams encoded audio chunks over this WebSocket.
On "end", the server concatenates the chunks, transcribes locally with
faster-whisper (or the stub), runs the (stub) classifier, and returns a
provisional ticket for operator review.

Protocol (server → client and client → server messages are JSON text,
audio is sent as binary frames):
    server: {"type":"ready", "session_id": "..."}
    client: <binary audio chunks>            # webm/opus from MediaRecorder
    client: {"type":"end"}                    # finish the utterance
    server: {"type":"result", ...VoiceTicketResult...}
    client: {"type":"cancel"}                 # abort, no ticket
"""
from __future__ import annotations

import json
import logging
import os
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.config import get_settings
from backend.schemas import VoiceTicketResult
from backend.services import tickets
from backend.services.stt import get_transcriber

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/voice", tags=["voice"])


@router.websocket("/ws")
async def voice_ws(ws: WebSocket) -> None:
    await ws.accept()
    settings = get_settings()
    os.makedirs(settings.audio_tmp_dir, exist_ok=True)

    session_id = uuid.uuid4().hex[:12]
    audio_path = os.path.join(settings.audio_tmp_dir, f"{session_id}.webm")
    chunks = bytearray()

    await ws.send_text(json.dumps({"type": "ready", "session_id": session_id}))
    logger.info("voice session %s started", session_id)

    try:
        while True:
            msg = await ws.receive()

            if msg.get("bytes") is not None:
                chunks.extend(msg["bytes"])
                continue

            if msg.get("text") is not None:
                data = json.loads(msg["text"])
                mtype = data.get("type")

                if mtype == "cancel":
                    logger.info("voice session %s cancelled", session_id)
                    await ws.send_text(json.dumps({"type": "cancelled"}))
                    break

                if mtype == "end":
                    if not chunks:
                        await ws.send_text(
                            json.dumps({"type": "error", "message": "no audio received"})
                        )
                        continue

                    with open(audio_path, "wb") as fh:
                        fh.write(chunks)

                    result = _process(session_id, audio_path)
                    await ws.send_text(
                        json.dumps({"type": "result", **json.loads(result.model_dump_json())})
                    )
                    break

    except WebSocketDisconnect:
        logger.info("voice session %s disconnected", session_id)
    finally:
        if os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except OSError:
                pass


def _process(session_id: str, audio_path: str) -> VoiceTicketResult:
    tr = get_transcriber().transcribe_file(audio_path)
    classification = tickets.classify(tr.text)
    ticket_number = tickets.next_ticket_number()
    logger.info("voice session %s → %s (stub_stt=%s)", session_id, ticket_number, tr.stub)
    return VoiceTicketResult(
        session_id=session_id,
        transcript=tr.text,
        language=tr.language,
        classification=classification,
        ticket_number=ticket_number,
        status="pending_review",
        stub_stt=tr.stub,
    )
