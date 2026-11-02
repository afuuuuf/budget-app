# Backend Backlog

Notes logged 2026-10-27 after a backend review, before moving to frontend work.
Items are roughly in priority order. This file is updated as work lands; see Recent History
at the bottom for items resolved since the original review. Checked `[x]` items are done.

## Medium priority (backend completeness)

- [ ] **No tests.** `pytest` is installed but there are zero tests. Add at least repo/service
      tests for the core paths (dashboard totals, savings goal auto-complete, auth token flow).

## Low priority / future

- [ ] **No SQLAlchemy `relationship()` objects.** Models use bare `ForeignKey` columns and manual repo
      queries; there is no ORM object-graph navigation (e.g. `user.budgets`). Works fine — cosmetic/cleanup.

## Recent History (since the 2026-10-27 review)

- 2026-11-03 — unified `Category`/`BudgetType` into one enum; finance columns all `BigInteger` minor units.
- 2026-11 — net savings rate & net cash flow derived in `TransactionService`; dashboard `currentBalance`
  and `netSavingsRate` return correct values. Money fields across the API moved `float` → `int`.
- 2026-11 — `src/services/impl/` collapsed into concrete services in `src/services/`; dashboard service
  no longer depends on `SavingsService`.
