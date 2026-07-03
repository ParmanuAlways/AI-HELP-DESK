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
- [ ] **Voice intake approach** — A (browser WebRTC), B (Asterisk fake
      PBX + SIP softphone), or C (record & upload). See
      `docs/voice_intake_poc.md` §3.
- [ ] Agentic scope: helpdesk-only vs automation into apps; read-only
      diagnostic probing allowed?; advise-only vs gated remediation.
      See `docs/agentic_workflows.md` §6.

## Foundation work (not started)
- [ ] Rebuild empty backend skeleton (config, models matching schema,
      routers, LLM/embedding service interfaces) — every .py is currently empty.
- [ ] Confirm embedding dimension (schema says vector(1024); README also
      mentions 768). Pick the model, make it consistent.
- [ ] Seed script: parse `knowledge_base/applications/*.md` → embeddings → Postgres.
