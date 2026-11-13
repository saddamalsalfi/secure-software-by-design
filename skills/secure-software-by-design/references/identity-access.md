# Identity, sessions, and permissions

Read only when this domain intersects the scoped change. Every applicable control is mandatory; verify implementation and negative cases.

- **MUST** Enforce authentication and authorization independently on every relevant operation and object, including field-level access, ownership, tenant scope, files, search, aggregates, subscriptions, workers, and bulk endpoints.
- **MUST** Prevent IDOR/BOLA, function-level bypass, mass assignment, horizontal/vertical privilege escalation, and confused-deputy behavior. Never trust client-supplied roles, prices, ownership, or tenant identifiers without server-side checks.
- **MUST** Use mature authentication libraries; protect enrollment, login, account recovery, invitation, account linking, MFA, and sensitive account changes. Bound attempts without creating easy account-lockout denial of service.
- **MUST** Use secure password hashing with library-supported parameters appropriate to the environment. Generate tokens with cryptographic randomness; limit scope and lifetime; avoid disclosure in URLs, logs, analytics, and errors.
- **MUST** Rotate sessions after authentication and privilege changes, invalidate them on logout and relevant account events, and configure cookie attributes to the actual deployment. Implement CSRF protection for cookie-authenticated state changes; SameSite is supporting protection.
- **MUST** Validate token signature, allowed algorithm, issuer, audience, expiry, and token purpose. Implement OAuth/OIDC protections through supported libraries, including redirect validation, state, nonce, and PKCE as applicable.

## Revocation
- **MUST** verify revocations propagate to caches, sessions, workers, exports, and long-lived connections according to the security requirements. Generate separate read/write field authorization rows.
