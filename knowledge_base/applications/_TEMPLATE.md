# Application: <Name>

> Knowledge-base source file for the AI Help Desk application registry.
> Each section maps directly to a database table so it can be parsed,
> embedded, and seeded automatically. Keep entries short and phrased the
> way real users talk — these lines become pgvector embeddings.

## 1. Identity  `→ applications`

| Field         | Value |
| :---          | :---  |
| Name          |       |
| Description   |       |
| Owning Team   |       |
| Contact       |       |

## 2. Purposes  `→ app_purposes` (embedded)

What the application is used for, one purpose per line, phrased how a
user would describe it. Used for semantic matching when a complaint
describes *what they were trying to do*.

- ...

## 3. Symptoms  `→ app_symptoms` (embedded)

Common complaint phrasings, one per line. Include English, Hindi, and
Hinglish variants — each line is embedded separately, so more phrasing
variety = better matching.

- ...

## 4. Dependencies  `→ app_dependencies`

Systems this application depends on, and the nature of each dependency.
The nature drives conditional expansion (e.g. a `login` fault pulls in
`authentication` dependencies).

| Depends On | Dependency Nature | When it matters |
| :---       | :---              | :---            |
|            |                   |                 |

## 5. Applicable Fault Types

Which fault categories can occur for this app (used to constrain the
classifier's choices).

- login / authentication
- performance / slowness
- functional error
- data issue
- access / permission
- outage / unreachable

## 6. Routing & Escalation

| Severity | Route To | Notes |
| :---     | :---     | :---  |
|          |          |       |

## 7. Known Recurring Issues

Chronic problems with their standard fixes (feeds suggested-resolution
RAG later).

- ...

## 8. Open Questions

- ...
