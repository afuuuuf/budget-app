from ..routers.dto import DashboardDto
from ..schemas import responses


class DashboardMapper:
    def to_resp(self, dto: DashboardDto) -> responses.DashboardListResponse:
        return responses.DashboardListResponse(
            totalIncome=dto.total_income,
            totalExpenses=dto.total_expenses,
            currentBalance=dto.current_balance,
            netSavingsRate=dto.net_savings_rate,
            budgetOverview=[
                responses.BudgetOverviewItem(
                    budgetType=budget_type,
                    amount=amount,
                    spent=spent,
                    remaining=remaining,
                )
                for budget_type, amount, spent, remaining in dto.budget_overview
            ],
            categorySpending=[
                responses.CategorySpendingItem(category=category, amount=amount)
                for category, amount in dto.category_spending
            ],
        )
