from pydantic import BaseModel


class DashboardListResponse(BaseModel):
    totalIncome: float
    totalExpenses: float
    currentBalance: float
    savingsProgress: float
    budgetOverview: float
    categorySpending: float