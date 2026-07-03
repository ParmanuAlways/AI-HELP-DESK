"""POC admin authentication.

Local username/password from settings; successful login issues an opaque
bearer token held in memory with an expiry. Deliberately minimal — in
production this whole module is replaced by Keycloak SSO (JWT
verification), which is how the org's other applications authenticate.
"""
from __future__ import annotations

import hmac
import secrets
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.config import get_settings

_tokens: dict[str, datetime] = {}  # token -> expiry
_bearer = HTTPBearer(auto_error=False)


def login(username: str, password: str) -> str | None:
    s = get_settings()
    ok = hmac.compare_digest(username, s.admin_username) and hmac.compare_digest(
        password, s.admin_password
    )
    if not ok:
        return None
    token = secrets.token_urlsafe(32)
    _tokens[token] = datetime.utcnow() + timedelta(minutes=s.admin_session_minutes)
    return token


def logout(token: str) -> None:
    _tokens.pop(token, None)


def require_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> str:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = credentials.credentials
    expiry = _tokens.get(token)
    if expiry is None or expiry < datetime.utcnow():
        _tokens.pop(token, None)
        raise HTTPException(status_code=401, detail="Session expired — login again")
    return token
