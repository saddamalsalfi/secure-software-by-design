# Full discovery, prioritization, and verification

Use this workflow for Mode B and for broad brownfield changes (Mode C + B).

## 1. Discover and model before implementation

Inspect project instructions, manifests, lockfiles, entry points, configuration, deployment definitions, existing security tests, and relevant code. Never print secrets while inspecting files.

Identify:
- Assets, data classifications, retention requirements, credentials, and security invariants.
- Actors, roles, service identities, tenants, administrators, guests, and attackers.
- Entry points: forms, APIs, RPC, GraphQL, WebSocket, webhooks, uploads, imports, CLI, IPC, deep links, background workers, scheduled jobs, hardware interfaces, and third parties.
- Trust boundaries and data flows through browsers, servers, databases, storage, caches, queues, external services, and build infrastructure.
- Exposure, authentication methods, privilege levels, concurrency, failure paths, and deployment assumptions.

When access policy applies, build an authorization matrix: actor × action × resource × tenant × field. Include ownership, lifecycle state, bulk operations, background execution, export, and administration as relevant.

For each relevant boundary, consider spoofing, tampering, repudiation, disclosure, denial of service, privilege escalation, privacy violations, and business abuse. Trace attacker-controlled input to sensitive operations. Treat stored records and external responses as potentially untrusted too.

Record uncertainties; inspect available evidence before asking questions. Ask only for decisions that materially affect safe implementation, and continue independent work.

## 2. Prioritize risks and maintain coverage

For a full review, use the project's existing report location or create a scoped security review document when files are requested. For a review-only conversation, report findings inline. Use the templates below as needed.

For each finding record: identifier, affected surface, threat scenario, evidence, impact, likelihood and exposure, priority, control, verification method/result, status, and residual risk. Add CWE identifiers only when verified. Distinguish confirmed vulnerabilities, suspected weaknesses, design risks, and hardening suggestions.

Use these priorities with documented rationale:
- P0: active exposure or a credible immediate path to severe compromise; contain before release.
- P1: high-impact exploitable weaknesses, including authorization bypass, injection into sensitive sinks, credential disclosure, or cross-tenant access; fix before release of affected functionality.
- P2: meaningful weaknesses requiring constrained conditions; schedule remediation with an owner and deadline.
- P3: low-impact improvements; track without overstating severity.

Do not assign severity solely from a vulnerability name. Evaluate exploit prerequisites and business impact. Classify each applicable control as implemented-and-verified, implemented-but-unverified, missing, or not-applicable-with-reason. A checklist item is not proof. Never silently accept risk on the user's behalf; clearly identify release blockers and any explicit risk acceptance.

## 3. Verify and implement when requested

When implementation is in scope, integrate controls into the actual code, schemas, migrations, configuration, and deployment templates within scope. Centralize reusable enforcement while preserving checks at each relevant boundary. Preserve intended behavior and explain any security-driven API or workflow change.

Use the stack's official documentation and authoritative security sources to resolve version-specific behavior. Consult current OWASP ASVS/API guidance, CWE, platform advisories, NIST SSDF, and relevant vendor documentation as applicable; record versions/dates for standards-based claims. Do not claim compliance from checklist completion.

Run applicable available checks: static analysis, secret detection, dependency analysis, configuration/IaC analysis, unit/integration tests, and bounded defensive checks in an isolated test environment. Use targeted fuzzing or sanitizers for parsers and native boundaries. Never install/run tools blindly or interpret a clean scanner report as proof of security.

Add meaningful negative regression tests for changed security behavior. Include anonymous access, wrong user, wrong role, wrong tenant, protected field mutation, malformed/boundary input, expired/replayed tokens, invalid transitions, concurrency, and failure paths as relevant. Confirm rejected requests create no unauthorized side effects, and valid requests still work. Verify each sensitive response reveals only permitted data.

Inspect diffs for bypass paths and security regressions. Rerun affected checks after fixes. Report unavailable checks, missing runtime access, assumptions, and unresolved findings plainly; never fabricate test results.


## 4. Evidence and maintenance
MUST record standard versions/access dates and distinguish reviewed configuration from verified deployed state. MUST track risk acceptance with an authorized owner, rationale, scope, compensating controls, and expiry. MUST NOT silently accept risk. MUST use safe rollback and test recovery.
### Report templates

| ID | Boundary / evidence | Impact and priority | Control / status | Verification result | Residual risk or next step |
|---|---|---|---|---|---|
| SEC-001 | … | … | … | … | … |

| Actor / role | Resource and action | Ownership, tenant, and state rule | Read/write fields | Server-side enforcement |
|---|---|---|---|---|
| … | … | … | … | … |

For a staged rollout, record compatibility tests, temporary containment, redacted telemetry, owner and deadline, promotion criteria, and a rollback that preserves essential security controls. Shadow checks do not remediate active exposure.
