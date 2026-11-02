from pydantic import BaseModel


class BudgetOverviewItem(BaseModel):
    budgetType: str
    amount: int
    spent: int
    remaining: int


class CategorySpendingItem(BaseModel):
    category: str
    amount: int


class DashboardListResponse(BaseModel):
    totalIncome: int
    totalExpenses: int
    currentBalance: int
    savingsProgress: float
    budgetOverview: list[BudgetOverviewItem]
    categorySpending: list[CategorySpendingItem]
