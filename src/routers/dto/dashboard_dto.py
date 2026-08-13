from dataclasses import dataclass


@dataclass
class DashboardDto:
    total_income: float
    total_expenses: float
    current_balance: float
    savings_progress: float
    budget_overview: list[tuple[str, float, float, float]]  # (budget_type, amount
    category_spending: list[tuple[str, float]]