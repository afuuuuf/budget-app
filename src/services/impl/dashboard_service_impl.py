from ...mappers import DashboardMapper
from ...repository import BudgetRepository, TransactionRepository
from ...routers.dto import DashboardDto
from ..dashboard_service import DashboardService


class DashboardServiceImpl(DashboardService):
    def __init__(
        self,
        transaction_repo: TransactionRepository,
        budget_repo: BudgetRepository,
        dashboard_mapper: DashboardMapper,
    ):
        self.transaction_repo = transaction_repo
        self.budget_repo = budget_repo
        self.dashboard_mapper = dashboard_mapper

    def get_dashboard_details(self) -> DashboardDto:
        total_income = self.transaction_repo.sum_by_flow("INCOME")
        total_expenses = self.transaction_repo.sum_by_flow("EXPENSE")
        current_balance = total_income - total_expenses
        savings_progress = (
            (current_balance / total_income * 100) if total_income else 0.0
        )

        category_spending = self.transaction_repo.sum_by_category()
        spent_by_category = dict(category_spending)

        budget_overview = []
        for budget in self.budget_repo.list_for_current_month():
            spent = spent_by_category.get(budget.budget_type, 0.0)
            budget_overview.append(
                (budget.budget_type, budget.amount, spent, budget.amount - spent)
            )

        return DashboardDto(
            total_income=total_income,
            total_expenses=total_expenses,
            current_balance=current_balance,
            savings_progress=savings_progress,
            budget_overview=budget_overview,
            category_spending=category_spending,
        )
