# Backend Backlog

Notes logged 2026-10-27 after a backend review, before moving to frontend work.
Items are roughly in priority order. The user decided to tie `Budget`/`Transaction`
to a user in the future, so items relying on that are marked accordingly.

## High priority

- [x] **BUG: `/v1/dashboard` crashes — `BudgetRepository.list_for_current_month()` does not exist.**
  `src/services/impl/dashboard_service_impl.py:30` calls `self.budget_repo.list_for_current_month()`,
  but `BudgetRepository` only defines `list_all()`, `find_by_id`, `find_by_budget_type_and_month`,
  `save`, `update`, `delete`. The dashboard endpoint raises `AttributeError` at runtime.
  **FIXED 2026-10-27:** added `find_budget_by_month()` to the repo (filters `created_month` + `deleted_at IS NULL`),
  added `BudgetService.get_budget_list_by_month()` (abstract + impl), and rewired the dashboard to
  call the service instead of the repo. Dashboard router now injects `BudgetService`.
  Verified: ruff clean, app imports, ABC satisfied. Endpoint not yet exercised against a live DB.

## Medium priority (backend completeness)

- [ ] **No tests.** `pytest` is installed but there are zero tests (README admits it). Once work
      moves to the frontend, backend regressions are no longer caught by hand. Add at least repo/service
      tests for the core paths (dashboard totals, savings goal auto-complete, auth token flow).

- [ ] **Category vs BudgetType mismatch.** `Category` only defines `FOOD` and `ENTERTAINMENT`, while
      `BudgetType` has 5 values (BILLS, SHOPPING, TRANSPORTATION, ENTERTAINMENT, OTHERS). The dashboard
      cross-references spending per budget type, but categories and budget types are different enums and
      only align on `ENTERTAINMENT`. Dashboard `spent` per budget type is mostly 0 today.
      Needs a product decision: rename/reconcile, or keep separate and map explicitly.

## Low priority / future (tied to user-scoping decision)

- [ ] **`Transaction` and `Budget` are not scoped to a user** (no `user_id`). User confirmed this is
      intentional for now and will add later. When done, remember the next item.

- [ ] **`get_current_user` missing on transactions/budgets/dashboard routers.** `savings_routers` uses
      `Depends(get_current_user)` everywhere, but `transactions_routers`, `budget_routers`, and
      `dashboard_routers` do not require auth. Harmless today (not user-scoped), but becomes a real
      gap the moment user-scoping lands — add auth to those routers at the same time.

- [ ] **No SQLAlchemy `relationship()` objects.** Models use bare `ForeignKey` columns and manual repo
      queries; there is no ORM object-graph navigation (e.g. `user.budgets`). Works fine — cosmetic/cleanup.

## Polish

- [ ] **Misnomer:** `delete_transaction` in `savings_routers.py` actually deletes savings goals
      (name copied from the transactions router). Harmless, but rename to `delete_savings_goal`.
