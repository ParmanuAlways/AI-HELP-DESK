# Application: eOffice

> Status: **DRAFT — pending owner review.** Items marked `[TBC]` are
> unconfirmed drafts to be corrected/confirmed by the user.

## 1. Identity  `→ applications`

| Field         | Value |
| :---          | :---  |
| Name          | eOffice |
| Description   | Proprietary (non-NIC) application for day-to-day official correspondence and communication. |
| Owning Team   | eOffice support team |
| Contact       | IP (intercom) 23137845 |

**Type**: Proprietary / in-house build (not NIC eOffice).
**Authentication**: Direct LDAP integration — **not** on Keycloak SSO
(exception among the registered applications). Each user has their own
personal **I-Key** (physical hardware token) required to open the app.

**Ticket routing**: tickets are raised under the **category = eOffice**
and routed to the eOffice support team (IP 23137845). The application
name *is* the routing category.

## 2. Purposes  `→ app_purposes` (embedded)

- Sending and receiving official letters/messages between offices
  (delivery is instantaneous)
- Moving / forwarding a file to another officer for approval
  (near-instantaneous)
- Uploading and sharing documents
- Locating a file when it is not found — user provides a **reference
  number** and the **document type** (letter, note, etc.)
- Storing files in a personal **inbox** and **cabinet**

**Not** used for: chat/instant messaging, or broadcasting circulars/
notices (those are handled by other means).

## 3. Symptoms  `→ app_symptoms` (embedded)

Confirmed error categories from the owner. Each line is embedded
separately — English + Hinglish variants are included on purpose.

### Login / access — I-Key (physical token)
> The app opens only after **I-Key validation** (a physical hardware
> key). If the I-Key is not detected, the user cannot get in.
- Unable to login to eOffice
- eOffice me login nahi ho raha
- I-Key not detected / eOffice not opening after inserting I-Key
- I-Key detect nahi ho raha, app khul hi nahi raha
- Physical key inserted but eOffice not recognising it

### File not found / missing from inbox or cabinet
> When a file is missing the user typically quotes a reference number
> and the document type (letter, note, etc.).
- File not found in eOffice
- Some files missing from my inbox
- File not showing in cabinet
- File cabinet/inbox me nahi mil rahi
- Reference number daalne par bhi file nahi mil rahi

### Signing
- Unable to sign a file / document in eOffice
- Sign nahi ho raha
- Signing option not working / error while signing

### Document upload
- Unable to upload a document
- Document upload fail ho raha hai
- Attachment upload nahi ho raha / stuck

### Data loss
- Draft file got deleted
- Draft file apne aap delete ho gayi
- Saved draft missing

### Performance / availability
- eOffice is too sluggish / slow to open
- eOffice bahut slow khul raha hai, hang ho raha hai

## 4. Dependencies  `→ app_dependencies`

| Depends On | Dependency Nature | When it matters |
| :---       | :---              | :---            |
| I-Key hardware token + driver/middleware | authentication | App won't open / not detected → login **and** signing faults (same personal I-Key used for both) |
| LDAP / shared directory | authentication | eOffice binds **directly** to LDAP (not via Keycloak), but the directory is the **same backing store Keycloak uses**. A directory outage hits eOffice **and** all SSO apps → strong root-cause signal for a correlated login incident. |
| Sector/area network segment | connectivity | Sluggishness is typically localised to **one sector/area** → suspect that area's network, not the app server. |
| [TBC] file/document storage | storage | Document upload failures, missing files |
| [TBC] database server | data | Draft deletion / data-loss faults |
| [TBC] network / intranet | connectivity | Unreachable / sluggishness faults |

## 5. Applicable Fault Types

- login / authentication (incl. I-Key not detected)
- signing failure
- file-not-found / missing from inbox or cabinet
- document upload failure
- data issue / data loss (deleted drafts)
- performance / slowness
- outage / unreachable

## 6. Routing & Escalation

All eOffice tickets route to the **eOffice support team (IP 23137845)**.
Category = application name.

| Severity | Route To | Notes |
| :---     | :---     | :---  |
| All      | eOffice support team (IP 23137845) | [Severity thresholds TBC] |

## 7. Known Recurring Issues

- **I-Key not detected** — every user has their own personal I-Key
  (physical token). Typically a client-side/token issue: reseat/reinsert
  the I-Key, check the token driver/middleware on the user's machine.
  `[confirm exact fix steps]`
- **File not found in inbox/cabinet** — can be a genuine glitch, or the
  file is misplaced in the database. The eOffice support team locates /
  recovers it (user supplies the **reference number** + **document type**
  — letter, note, etc.).
- **Draft file deleted** — sometimes recoverable, decided **case to case**
  by the support team (not always recoverable).
- **Sluggish to open** — usually affects **one sector/area** at a time →
  investigate that area's network segment rather than the app server.
- **Can't sign** — signing uses the **same personal I-Key** as login, so
  treat alongside I-Key detection issues.

## 8. Open Questions (remaining)

1. Roughly **how many users / which units** use it? (severity calibration)
2. Where is it **hosted** (app server, DB server, document storage) — do
   we register those as separate infrastructure entries so an outage
   there can be flagged as the root cause?

## Resolved
- Owning team / routing: eOffice support team, IP 23137845, category = app name ✓
- Type: proprietary (non-NIC) ✓
- Auth: direct LDAP bind + per-user I-Key hardware token ✓
- I-Key: personal per user; used for **both** login and signing ✓
- LDAP: **shared directory with Keycloak** but eOffice binds directly,
  not via Keycloak → shared-directory outage = correlated multi-app signal ✓
- Features & error catalogue ✓
- File-not-found: glitch or DB-misplacement; support team locates it ✓
- Draft deleted: recoverable case-to-case (not guaranteed) ✓
- Sluggish: usually localised to one sector/area → area network segment ✓
