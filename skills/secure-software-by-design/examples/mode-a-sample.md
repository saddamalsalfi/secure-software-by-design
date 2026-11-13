# Mode A: endpoint-local object access repair

**Fictional gold example. Test names and results illustrate format only; never present them as executed evidence.**

Request: repair the missing ownership check in `src/records.py:get_record` without changing shared access policy. Existing architecture already defines owner-only record reads. This is a local implementation repair, not a redesign of identity or cross-tenant policy.

Triage: changed paths `src/records.py`, `tests/test_records.py`; added/deleted lines use `record.owner_id == principal.id`. The shared access policy is unchanged. Escalate to Mode B if the effective diff changes a shared invariant, such as who can read records across tenants.

Mode: A. Scope: record GET endpoint and its negative integration tests.
Readiness: ready-for-scoped-change (illustrative).

| ID | Surface | Threat / CWE | Priority | Status | Verification Evidence | Residual Risk |
|---|---|---|---|---|---|---|
| SEC-001 | GET /records/{id} | Other user's private record accessible by identifier; CWE not cited | P1 | implemented-and-verified | Fictional: owner-read passes; wrong-user and anonymous requests denied; private fields absent | Other endpoints were not audited |

SEC-001 classification: confirmed vulnerability in the fictional fixture. Impact: disclosure of private record data to an authenticated non-owner. Exposure: attacker knows or obtains an identifier. Control: existing owner-only rule enforced in the resource lookup; denied requests return the established not-found response. No state mutation.

Verification (fictional):
- VER-001: non-owner cannot read; `test_non_owner_read`; passed.
- VER-002: anonymous request cannot read; `test_guest_read`; passed.
- VER-003: owner can read authorized fields; `test_owner_read`; passed.
- VER-004: diff scan completed for tracked and explicit untracked scope; no candidates; passed, heuristic only.

Applicable gates passed in this fictional fixture: boundary control, P1 repair, private-field minimization, negative and valid flow tests. No deployment was performed; deployed behavior remains unverified. No docs/security-review.md created; no irrelevant-domain exclusions.
