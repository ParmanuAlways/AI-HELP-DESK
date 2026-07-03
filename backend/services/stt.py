"""Speech-to-text service (faster-whisper, fully local/offline).

Loads a local CTranslate2 whisper model. If faster-whisper or the model
is unavailable — or ``stt_stub`` is set (dev default) — it falls back to
a stub transcriber so the whole voice pipeline can be exercised without
the model present. This mirrors the project's graceful-degradation rule:
the voice layer must never hard-block on the AI model being installed.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

from backend.config import get_settings

logger = logging.getLogger(__name__)


@dataclass
class Transcription:
    text: str
    language: Optional[str] = None
    duration_sec: Optional[float] = None
    stub: bool = False


class _StubTranscriber:
    """Returns placeholder text so plumbing works without the model."""

    stub = True

    def transcribe_file(self, path: str) -> Transcription:
        import os

        size = os.path.getsize(path) if os.path.exists(path) else 0
        logger.warning("STT stub active — returning placeholder for %s (%d bytes)", path, size)
        return Transcription(
            text=(
                "[STT STUB] eOffice me login nahi ho raha, I-Key detect nahi kar raha. "
                "(Placeholder transcript — real faster-whisper not loaded.)"
            ),
            language="hi",
            duration_sec=None,
            stub=True,
        )


class _WhisperTranscriber:
    """Real faster-whisper backend."""

    stub = False

    def __init__(self) -> None:
        from faster_whisper import WhisperModel  # imported lazily

        s = get_settings()
        logger.info("Loading faster-whisper model=%s device=%s", s.whisper_model, s.whisper_device)
        self._model = WhisperModel(
            s.whisper_model, device=s.whisper_device, compute_type=s.whisper_compute_type
        )

    def transcribe_file(self, path: str) -> Transcription:
        # auto language detection handles English / Hindi / code-mixed Hinglish
        segments, info = self._model.transcribe(path, beam_size=5, vad_filter=True)
        text = " ".join(seg.text.strip() for seg in segments).strip()
        return Transcription(
            text=text,
            language=getattr(info, "language", None),
            duration_sec=getattr(info, "duration", None),
            stub=False,
        )


_transcriber = None


def get_transcriber():
    """Singleton transcriber; picks real backend or stub with fallback."""
    global _transcriber
    if _transcriber is not None:
        return _transcriber

    s = get_settings()
    if s.stt_stub:
        _transcriber = _StubTranscriber()
        return _transcriber

    try:
        _transcriber = _WhisperTranscriber()
    except Exception as exc:  # model or lib missing — degrade, don't crash
        logger.warning("faster-whisper unavailable (%s); falling back to STT stub", exc)
        _transcriber = _StubTranscriber()
    return _transcriber
