from dataclasses import dataclass


@dataclass
class DashboardDto:
    total_income: int
    total_expenses: int
    current_balance: int
    savings_progress: float
    budget_overview: list[tuple[str, int, int, int]]  # (budget_type, amount
    category_spending: list[tuple[str, int]]
