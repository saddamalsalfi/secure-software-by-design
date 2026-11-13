# APIs, browser boundaries, and network requests

Read only when this domain intersects the scoped change. Every applicable control is mandatory; verify implementation and negative cases.

- **MUST** Define request and response schemas and minimize returned fields. Apply per-principal and appropriate global limits, pagination, body limits, timeouts, concurrency limits, and query-cost limits.
- **MUST** Configure CORS narrowly; do not treat it as authorization. Protect WebSocket origins and message-level permissions. Validate `postMessage` origin, source, and payload.
- **MUST** Validate webhook signatures over the required raw representation; prevent replay and duplicate effects using bounded timestamps, identifiers, and atomic idempotency handling.
- **MUST** Prevent SSRF through destination allowlists where feasible, controlled egress, scheme/port restrictions, redirect revalidation, and checks against private, loopback, link-local, and metadata destinations. Account for IPv6, DNS rebinding, and DNS resolution/connect-time differences.
- **MUST** Review proxy trust, forwarded headers, host validation, request parsing consistency, request smuggling, redirect targets, cache keys, cache poisoning, cache deception, and caching of authenticated responses.
- **MUST** Use appropriate TLS, certificate verification, CSP, framing restrictions, MIME protection, referrer policy, and transport security after checking deployment compatibility. Do not introduce permissive exceptions as routine fixes.
