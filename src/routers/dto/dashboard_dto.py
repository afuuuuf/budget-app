from dataclasses import dataclass

from ...enums import Category


@dataclass
class DashboardDto:
    total_income: int
    total_expenses: int
    current_balance: int
    net_savings_rate: float
    budget_overview: list[tuple[Category, int, int, int]]  # (category, amount
    category_spending: list[tuple[Category, int]]
