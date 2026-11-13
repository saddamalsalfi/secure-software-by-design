# AI and agent features, when present

Read only when this domain intersects the scoped change. Every applicable control is mandatory; verify implementation and negative cases.

- **MUST** Treat prompts, retrieved documents, tool output, and model output as untrusted data. Keep authorization and policy enforcement outside the model.
- **MUST** Restrict tools, credentials, destinations, and data scope; require application-level controls for consequential actions. Prevent prompt injection from expanding privileges or leaking secrets.
- **MUST** Validate generated commands, code, queries, HTML, and structured outputs before use. Apply the same injection and output-encoding controls as any other external input.
- **MUST** Enforce retrieval tenant boundaries, upload controls, usage budgets, and logging privacy. Do not claim prompt wording alone prevents prompt injection.


## Context and tool isolation
- **MUST** minimize and redact data before building prompts, retrieval results, embeddings, or agent memory. Verify provider retention and logging controls before transmitting protected data. Never send unnecessary PII or secrets.
- **MUST** treat agent memory as untrusted. Keep trusted instructions distinguishable from retrieved content, without claiming delimiters enforce security.
- **MUST** verify hostile content cannot cause unauthorized tool calls, outbound requests, cross-tenant retrieval, or data access. Bound resources and enforce authorization outside the model.
- **MUST** apply package provenance controls to AI-generated imports and dependency proposals before installation.
