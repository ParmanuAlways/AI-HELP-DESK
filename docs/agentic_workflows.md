# Agentic Workflows — Design Draft

> Status: **DRAFT — pending scope decisions (see §6).**
>
> Goal: the AI layer should not only classify a complaint but *act* on
> it — plan multi-step work, call tools, verify results, and hand off to
> a human at defined gates. All of this runs fully offline against the
> local vLLM endpoint (Gemma) using OpenAI-compatible tool calling /
> guided JSON, so no framework with cloud dependencies is required.

## 1. Core runtime

A small in-house agent loop (no LangChain-class dependency — keeps the
air-gapped wheelhouse thin):

```
complaint/event ──▶ Agent loop:
                      1. LLM call (system prompt + state + tool schemas)
                      2. If tool_call → execute from allowlist → append result → goto 1
                      3. If final answer / gate reached → stop
                    bounded by: max N iterations, per-run token budget
```

Every run is persisted (new `agent_runs` + `agent_steps` tables): which
agent, every prompt/tool call/result, latency, outcome. This is the
audit trail (mandatory in this environment) and doubles as an eval set.

**Guardrails**

- Tools are an explicit allowlist per agent; tools are typed
  **read-only** vs **write**; write tools can require a human gate.
- Agent output is never auto-sent to a complainant; an operator approves.
- If vLLM is unreachable, intake degrades to plain form + queue for
  later AI enrichment — the agent layer must never block ticket creation.

## 2. Proposed agents (in build order)

### A. Triage Agent (first)
Runs on every new intake. Replaces the single-shot classifier with a loop:

| Tool | Type |
| :--- | :--- |
| `search_symptoms(text)` — pgvector over app_symptoms/purposes | read |
| `search_similar_tickets(text, status?)` | read |
| `get_dependencies(app_id, fault_type)` | read |
| `get_learning_examples(text)` — few-shot from corrections | read |
| `create_ticket(...)` / `link_to_ticket(ticket_no)` | write (gated on low confidence) |

Flow: identify app → check for duplicate/open incident → classify fault
type + severity → expand dependencies → create or link ticket → emit
confidence + reasoning for the operator console.

### B. Resolution Copilot Agent
Runs when an operator opens a ticket: pulls similar resolved tickets,
KB articles, and known recurring issues; drafts a suggested fix and a
reply; cites its sources (ticket numbers / article ids) so the operator
can verify.

### C. Correlation / Major-Incident Agent
Event-driven: when K similar tickets arrive within a time window, walk
the dependency graph for a common upstream (e.g. many login faults
across SSO apps ⇒ suspect Keycloak/LDAP), open a master ticket, link
children, notify the owning team.

### D. Knowledge Agent
On ticket close: draft a KB article from complaint + resolution notes,
run a duplicate check against existing articles, queue for human
approval before publishing.

### E. Diagnostic Agent — *scope decision needed*
Runs whitelisted **read-only** probes inside the network to enrich
tickets with facts: HTTP health-check of the affected app, LDAP bind
test, DB connectivity probe, disk/queue metrics endpoint. Strictly
allowlisted commands, no shell access, results attached to the ticket.
(Active remediation — service restarts, LDAP unlocks — is a separate,
later decision with per-action human approval.)

## 3. Tool-calling with Gemma on vLLM

- Use vLLM's OpenAI-compatible `/v1/chat/completions` with `tools=[...]`
  and, where reliability matters, **guided JSON** (structured output) so
  malformed calls can't occur.
- Keep tool schemas small and few per agent (5–7 max) — small models
  pick tools far more reliably from short menus.
- One retry with the validation error included, then fall back to the
  non-agentic single-shot path.

## 4. Where it lives in the codebase

```
backend/
├── agents/
│   ├── runtime.py      # generic loop, budgets, audit persistence
│   ├── tools.py        # typed tool registry (read/write, gates)
│   ├── triage.py       # Agent A
│   ├── copilot.py      # Agent B
│   ├── correlation.py  # Agent C
│   └── knowledge.py    # Agent D
└── services/llm.py     # thin OpenAI-compatible client (vLLM base_url from config)
```

## 5. Human-in-the-loop gates (defaults)

| Action | Gate |
| :--- | :--- |
| Create ticket, high confidence | auto, flagged for review |
| Create ticket, low confidence | operator confirms in console |
| Link as duplicate | operator confirms |
| Send reply to complainant | always operator-approved |
| Publish KB article | always operator-approved |
| Open major incident | auto-create, immediate notify |

## 6. Open scope decisions

1. Confirm scope: agentic workflows for the **Help Desk itself** (as
   designed here) — or also automation *inside* eOffice/other apps?
2. Diagnostic Agent: is read-only network probing from the helpdesk
   server acceptable in this environment?
3. Any future appetite for gated **remediation actions** (e.g. LDAP
   account unlock), or strictly advise-only?
4. Which agents matter most first? Proposed: A → B → C → D → E.
