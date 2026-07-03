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

- Sending and receiving official correspondence electronically
- Moving files between offices and marking them to officers `[TBC]`
- Writing notings and drafting letters on electronic files `[TBC]`
- Tracking the status and movement history of an official file `[TBC]`
- Diarising inward receipts / dak `[TBC]`

## 3. Symptoms  `→ app_symptoms` (embedded)

All lines below are **drafts `[TBC]`** based on typical correspondence
systems — confirm which apply and add real phrasings from past complaints.

### Login / authentication
- Unable to login to eOffice, credentials not accepted
- eOffice login page keeps redirecting / loops back to login
- eOffice me login nahi ho raha hai
- Password sahi hai phir bhi eOffice access denied dikha raha hai

### File movement / correspondence
- Unable to forward file to next officer
- File sent but not appearing in recipient's inbox
- File eOffice me stuck ho gayi hai, aage nahi ja rahi
- Receipt / dak diarise nahi ho raha

### Functional
- Unable to upload attachment / attachment fails to open
- Draft not saving, noting disappeared after save
- Digital signature (DSC) token not detected while signing `[TBC — is DSC signing used?]`

### Performance / availability
- eOffice is very slow, pages taking long to load
- eOffice site not opening at all / server error
- eOffice bahut slow chal raha hai

## 4. Dependencies  `→ app_dependencies`

| Depends On | Dependency Nature | When it matters |
| :---       | :---              | :---            |
| LDAP Directory | authentication | Login faults expand to LDAP directly (no Keycloak in path) |
| [TBC] file/document storage | storage | Attachment upload/open faults |
| [TBC] database server | data | Data loss / save failures |
| [TBC] network / intranet | connectivity | Unreachable / slowness faults |

## 5. Applicable Fault Types

- login / authentication
- performance / slowness
- functional error (file movement, noting, drafting)
- data issue (attachments, lost drafts)
- access / permission (role not assigned, section not visible)
- outage / unreachable

## 6. Routing & Escalation

| Severity | Route To | Notes |
| :---     | :---     | :---  |
| [TBC]    | [TBC]    |       |

## 7. Known Recurring Issues

- [TBC — e.g. "account locks after N failed attempts, fix = LDAP unlock by admin"]

## 8. Open Questions

1. Which team owns eOffice and what is the contact (name/phone/email)?
2. Is this NIC eOffice or an in-house build? Which modules are deployed
   (eFile, receipts/dak, leave, KMS)?
3. Is DSC / digital-signature signing used? (frequent complaint source)
4. Is the LDAP that eOffice binds to the same directory Keycloak
   federates from for the other apps, or a separate one? (If shared, an
   LDAP outage hits eOffice *and* all SSO apps — strong root-cause signal.)
5. Roughly how many users / which units use it? (severity calibration)
6. What are the 3–5 most frequent real complaints received about it?
7. Where is it hosted (app server, DB server) — do we register those as
   separate infrastructure "applications" for dependency expansion?
