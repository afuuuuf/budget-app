from pydantic import BaseModel


class BudgetOverviewItem(BaseModel):
    budgetType: str
    amount: float
    spent: float
    remaining: float


class CategorySpendingItem(BaseModel):
    category: str
    amount: float


class DashboardListResponse(BaseModel):
    totalIncome: float
    totalExpenses: float
    currentBalance: float
    savingsProgress: float
    budgetOverview: list[BudgetOverviewItem]
    categorySpending: list[CategorySpendingItem]
