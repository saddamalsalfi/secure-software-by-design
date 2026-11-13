---
name: secure-software-by-design
description: Design, implement, review, or remediate defensive software controls. Use for threat modeling, security-sensitive changes, or release verification involving authorization, tenancy, APIs, data handling, dependencies, CI/CD, native code, or AI tools.
license: MIT
---

# Secure Software by Design

## 1. Define the boundary

Identify the requested outcome, trusted roles, sensitive data, entry points, and code that enforces the relevant invariant. Inspect callers and alternate paths (bulk actions, workers, exports, caches) only when they share that invariant. Treat inputs and retrieved content as untrusted. Use synthetic fixtures in an isolated test environment; do not probe live systems or develop exploit payloads. For a review, report evidence and remediation without editing unless implementation is requested.

## 2. Choose the smallest suitable workflow

| Mode | Choose when | Deliver |
|---|---|---|
| A — Bounded change | The affected boundary is local and the existing security policy stays intact. | Inline findings, scoped change, and verification. |
| B — Full design | New architecture, broad audit, or changes to shared authorization, tenant isolation, sensitive data lifecycle, privileged integrations, or security-critical release controls. | [Full workflow](references/full-workflow.md), a security review, and an authorization matrix when access policy applies. |
| C — Brownfield | Existing callers need compatibility or enforcement must be staged. | Characterization tests, containment, and [rollout and recovery criteria](references/full-workflow.md#report-templates). Add B deliverables if a shared invariant changes. |

Inspect relevant old/new paths and the effective diff, including new files and the intended base. Escalate based on what changes in behavior or exposure, not filenames or keywords. Reassess the mode if the change crosses another trust boundary. If the diff is unavailable, label the assessment partial. Do not expand a narrow task into a repository-wide rewrite.

## 3. Load only applicable references

| Surface | Reference |
|---|---|
| Input schemas, escaping, queries, execution | [Inputs and injection prevention](references/inputs-injection.md) |
| Identity, permissions, sessions, tenancy | [Identity and access](references/identity-access.md) |
| HTTP, browsers, outbound requests, webhooks | [Web and API](references/web-api.md) |
| Uploads, paths, archives, parsers | [Files and parsers](references/files-parsers.md) |
| Privacy, deletion, secrets, cryptography | [Privacy and data](references/privacy-data.md) |
| Transactions, concurrency, availability | [Logic and availability](references/logic-availability.md) |
| Native, mobile, desktop, embedded | [Native and embedded](references/native-embedded.md) |
| Packages, CI/CD, infrastructure | [Supply chain and infrastructure](references/supply-chain-infra.md) |
| LLMs, tools, retrieval, context | [AI agents](references/ai-agents.md) |

## 4. Verify and report

- Use [release verification](references/release-verification.md) to select checks. Test valid flows and applicable denial/failure paths; assert both the response and the absence of unauthorized side effects. Keep protections enabled.
- Use the [verification helpers](references/verification-tools.md) when their prerequisites and scope fit. The diff scanner is heuristic. Registry metadata does not establish dependency trust. Record skipped or inconclusive checks rather than treating them as passes.
- For each finding, give the affected boundary, evidence, impact and priority, fix, verification result, and residual risk. If a critical or high-impact weakness remains, mark the affected change blocked and name the next action. Do not infer deployed behavior from local tests.
- For a bounded example, see [Mode A](examples/mode-a-sample.md). Its evidence is fictional.

Use the user's language for the report unless they ask for a different language.
