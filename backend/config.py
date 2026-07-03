"""Application configuration.

All external endpoints (LLM, DB) and model paths are settings, never
hardcoded — so the same code runs in dev (mocked/stubbed) and in the
air-gapped enclave (real vLLM + local models) by changing env vars only.
"""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HELPDESK_", env_file=".env", extra="ignore")

    # --- App ---
    app_name: str = "AI Help Desk"
    debug: bool = True

    # --- LLM (vLLM, OpenAI-compatible) ---
    # In the enclave: point at the vLLM server serving Gemma.
    llm_base_url: str = "http://localhost:8000/v1"
    llm_model: str = "gemma"
    llm_api_key: str = "not-needed-local"

    # --- Speech-to-text (faster-whisper, local) ---
    # Path to a local CTranslate2 whisper model dir, or a model size name.
    whisper_model: str = "small"
    whisper_device: str = "cpu"
    whisper_compute_type: str = "int8"
    # When true, skip loading whisper and use the stub transcriber (dev).
    stt_stub: bool = True

    # --- Database (PostgreSQL + pgvector) ---
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/helpdesk"

    # --- Voice POC ---
    # Where streamed call audio is buffered before transcription.
    audio_tmp_dir: str = "/tmp/helpdesk_audio"


@lru_cache
def get_settings() -> Settings:
    return Settings()
