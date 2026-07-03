# Application: Keycloak (SSO)

> Status: **DRAFT — pending owner review.** Shared authentication
> dependency for registered applications (exception: eOffice, which
> logs in directly against LDAP and is not on Keycloak currently). When a login-type fault is
> reported against any app, the dependency expander pulls this in as a
> possible root cause; if multiple apps report login faults together,
> Keycloak/LDAP is the probable primary.

## 1. Identity  `→ applications`

| Field         | Value |
| :---          | :---  |
| Name          | Keycloak SSO |
| Description   | Central single-sign-on identity provider for all applications; federates credentials from the LDAP directory. |
| Owning Team   | [TBC] |
| Contact       | [TBC] |

## 2. Purposes  `→ app_purposes` (embedded)

- Single sign-on login for all internal applications
- Central authentication and session management

## 3. Symptoms  `→ app_symptoms` (embedded)

- Login not working on any application `[TBC]`
- SSO page not opening / stuck at redirect after entering password `[TBC]`
- Kisi bhi application me login nahi ho raha `[TBC]`
- Session expires immediately after login `[TBC]`

## 4. Dependencies  `→ app_dependencies`

| Depends On | Dependency Nature | When it matters |
| :---       | :---              | :---            |
| LDAP Directory | authentication | Credential validation failures |

## 5. Applicable Fault Types

- login / authentication
- outage / unreachable
- performance / slowness

## 8. Open Questions

1. Owning team and contact?
2. Single Keycloak realm for all apps, or per-app realms?
3. Is LDAP federation read-only, or are passwords managed in Keycloak?
