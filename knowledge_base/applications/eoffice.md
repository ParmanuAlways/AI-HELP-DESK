# Application: eOffice

> Status: **DRAFT — pending owner review.** Items marked `[TBC]` are
> unconfirmed drafts to be corrected/confirmed by the user.

## 1. Identity  `→ applications`

| Field         | Value |
| :---          | :---  |
| Name          | eOffice |
| Description   | Proprietary (non-NIC) application for day-to-day official correspondence and communication. |
| Owning Team   | [TBC — name of section/cell] |
| Contact       | IP (intercom) 23137845 |

**Type**: Proprietary / in-house build (not NIC eOffice).
**Authentication**: Direct LDAP integration — **not** on Keycloak SSO
(exception among the registered applications).

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
| I-Key hardware token + driver/middleware | authentication | App won't open / not detected → login & signing faults |
| LDAP Directory | authentication | Login faults expand to LDAP directly (no Keycloak in path) |
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

| Severity | Route To | Notes |
| :---     | :---     | :---  |
| [TBC]    | [TBC]    |       |

## 7. Known Recurring Issues

- [TBC — e.g. "account locks after N failed attempts, fix = LDAP unlock by admin"]

## 8. Open Questions

1. **Owning team name** — the section/cell that supports eOffice
   (contact IP 23137845 is recorded; need the team name for routing).
2. **I-Key ↔ signing**: is the file *signing* done with the **same I-Key**
   that opens the app, or a separate DSC/certificate? (Decides whether
   "can't sign" and "I-Key not detected" share a root cause.)
3. **File-not-found**: when a file is missing from inbox/cabinet, is it
   usually (a) a genuine bug/data issue, or (b) it moved to someone else
   and the user just needs help locating it? (Changes fault type + fix.)
4. Is the eOffice LDAP the **same directory** Keycloak federates from for
   the other apps, or a separate one? (Shared → an LDAP outage hits
   eOffice *and* all SSO apps: strong root-cause signal.)
5. Roughly **how many users / which units** use it? (severity calibration)
6. **Known fixes** for the common ones — e.g. I-Key not detected → reinsert
   / reinstall token driver? Sluggish → server-side or client-side?
7. Where is it **hosted** (app server, DB server, document storage) — do
   we register those as separate infrastructure entries so an outage
   there can be flagged as the root cause?
