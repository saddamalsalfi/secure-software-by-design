# Inputs, forms, and injection

Read only when this domain intersects the scoped change. Every applicable control is mandatory; verify implementation and negative cases.

- **MUST** Validate server-side at every trust boundary using explicit schemas: type, size, range, format, enum, nesting depth, collection count, required fields, and semantic relationships. Reject unexpected writable fields and ambiguous parsing where appropriate.
- **MUST** Normalize deliberately and consistently before validation; avoid double decoding, parser mismatches, duplicate parameter ambiguity, unsafe coercion, integer overflow, and Unicode/path normalization bypasses.
- **MUST** Treat browser validation as usability only. Use parameterized queries, safe query builders, contextual output encoding, safe DOM APIs, and dedicated allowlist sanitization only where rich HTML is required.
- **MUST** Avoid shell invocation, dynamic evaluation, untrusted template execution, unsafe deserialization, and external XML entities. If a process must run, fix the executable, constrain arguments and privileges, and prevent option injection.
- **MUST** Evaluate SQL/NoSQL/LDAP/XPath injection, command/code/template injection, XSS, CRLF/header/log injection, CSV formula injection, prototype pollution, and DOM clobbering where relevant. Do not use a generic escape function as a universal defense.
