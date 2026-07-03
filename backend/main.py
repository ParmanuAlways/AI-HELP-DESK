"""AI Help Desk — FastAPI entry point.

POC scope: wires up the voice-intake vertical slice (WebRTC → WebSocket →
STT → ticket) and serves the static voice demo page. Admin/ticket routers
and the real AI pipeline are added incrementally behind stable seams.
"""
from __future__ import annotations

import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.config import get_settings
from backend.routers import voice

logging.basicConfig(level=logging.INFO)

settings = get_settings()
app = FastAPI(title=settings.app_name)

# Dev CORS: the "caller" PC opens the page over the LAN. Tighten in prod.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(voice.router)

_FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "voice_poc")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "app": settings.app_name, "stt_stub": settings.stt_stub}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(os.path.join(_FRONTEND_DIR, "index.html"))


# Serve the static voice-POC assets (index.html, app.js) if present.
if os.path.isdir(_FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=_FRONTEND_DIR), name="static")
