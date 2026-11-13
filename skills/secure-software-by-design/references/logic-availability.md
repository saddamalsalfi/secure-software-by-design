# Logic, concurrency, and availability

Read only when this domain intersects the scoped change. Every applicable control is mandatory; verify implementation and negative cases.

- **MUST** Model valid state transitions and enforce server-side invariants for payments, balances, credits, quotas, approvals, discounts, inventory, and ownership.
- **MUST** Test replay, retries, duplicate messages, reordered events, negative/boundary values, race conditions, TOCTOU, double spend, and partial failure.
- **MUST** Use atomic operations, constraints, transactions, locking, and idempotency appropriate to the invariant. Bound retries, fan-out, queues, recursion, regex complexity, allocations, and expensive work.
- **MUST** Define degraded-mode behavior without authorization bypass; test resource exhaustion safely in isolation. Prevent shared caches and rate limits from causing tenant leaks or uncontrolled cross-user interference.

## Transaction details
- **MUST** bind idempotency keys to actor, tenant, operation, and request semantics. VERIFY failures and rejection leave no unauthorized partial state.
