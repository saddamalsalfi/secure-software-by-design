# Data, secrets, and cryptography

Read only when this domain intersects the scoped change. Every applicable control is mandatory; verify implementation and negative cases.

- **MUST** Minimize collection, access, retention, and exported data. Protect backups, replicas, caches, logs, search indexes, temporary files, and analytics as well as primary storage.
- **MUST** Keep secrets out of source, client bundles, images, fixtures, error messages, and logs. Use environment-appropriate secret management with scoped access and rotation procedures.
- **MUST** Use established authenticated encryption and verified transport; manage key generation, storage, access, rotation, and nonce uniqueness. Never hardcode algorithms or parameter values from memory when current guidance must be verified.
- **MUST** Scope database accounts, use constraints and transactions for invariants, protect migrations, and verify tenant isolation at each query boundary. Make deletion and retention behavior explicit.
- **MUST** Redact sensitive values from diagnostics. Return safe errors while preserving useful restricted operational evidence.

## Technical privacy enforcement
- **MUST** minimize fields at the query and DTO/serializer boundary; avoid fetching entire records merely to redact them later where narrow selection is possible. Enforce per-role and per-tenant masking and omission.
- **MUST** use allowlisted structured logging and redact secrets/PII in telemetry, traces, crash reports, exception payloads, query strings, attachments, CI logs, and model prompts. VERIFY nested values and error paths. Prefer synthetic fixtures and sanitized excerpts.
- **MUST** enforce tenant-scoped access and cryptographic boundaries where the threat model requires them; bind key selection and encryption context to server-verified tenant identity. Document key granularity. Shared disk encryption is not tenant cryptographic isolation or authorization.
- **MUST** implement verifiable hard deletion or crypto-shredding covering primary records, files, derived indexes, caches, exports, replicas, and processors. Define retention, legal holds, immutable backup expiry, and reapplication of deletion after restores.
- **MUST** verify destruction of applicable keys, key copies and wrapping paths before claiming crypto-shredding; account for plaintext copies and shared-key data. Retain minimal deletion evidence without deleted content.
