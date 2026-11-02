from pydantic import BaseModel

from ...enums import Category


class BudgetOverviewItem(BaseModel):
    category: Category
    amount: int
    spent: int
    remaining: int


class CategorySpendingItem(BaseModel):
    category: Category
    amount: int


class DashboardListResponse(BaseModel):
    totalIncome: int
    totalExpenses: int
    currentBalance: int
    netSavingsRate: float
    budgetOverview: list[BudgetOverviewItem]
    categorySpending: list[CategorySpendingItem]
