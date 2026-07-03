# Project TODO / Backlog

Running list of pending inputs and decisions. Updated as we go.

## Pending inputs from owner
- [ ] **Faults PDF** — owner to share a PDF containing all faults. On
      arrival: parse → extract real complaint phrasings → map to apps &
      fault types → fold into each app's KB file → wire cross-app
      (LDAP / I-Key / network) patterns into the dependency graph.
- [ ] eOffice calibration (non-blocking): user count / units; hosting
      infra (app/DB/storage servers) to register as infrastructure apps.
- [ ] Next applications: names, one-line purpose, and auth method each.

## Decisions needed
- [x] **Voice intake approach** — CHOSEN: browser WebRTC. Asterisk/SIP
      deferred to real-phone phase. See `docs/voice_intake_poc.md` §3.
  - [x] Sub-decision: `getUserMedia + MediaRecorder + WebSocket`
        (per-utterance transcription). Built & tested.
  - [x] Voice POC vertical slice implemented (mic→WS→STT stub→ticket).
        See `docs/voice_intake_poc.md` §5a.
  - [ ] Swap stub → real faster-whisper (needs local model + install).
  - [ ] Replace keyword classifier stub → real embed+pgvector+LLM pipeline.
  - [x] Persist tickets to DB (SQLite dev / Postgres enclave via
        HELPDESK_DATABASE_URL) — SQLModel Ticket table.
  - [x] Admin login + faults console at /admin (POC local creds via
        HELPDESK_ADMIN_USERNAME/PASSWORD; Keycloak SSO in production).
  - [ ] Operator review actions (approve/edit/close ticket) in admin UI (HITL).
- [ ] Agentic scope: helpdesk-only vs automation into apps; read-only
      diagnostic probing allowed?; advise-only vs gated remediation.
      See `docs/agentic_workflows.md` §6.

## Foundation work (not started)
- [ ] Rebuild empty backend skeleton (config, models matching schema,
      routers, LLM/embedding service interfaces) — every .py is currently empty.
- [ ] Confirm embedding dimension (schema says vector(1024); README also
      mentions 768). Pick the model, make it consistent.
- [ ] Seed script: parse `knowledge_base/applications/*.md` → embeddings → Postgres.
