from ...enums import TransactionFlow
from ...mappers import DashboardMapper
from ...routers.dto import DashboardDto
from ...services import BudgetService, DashboardService, TransactionService
from ...utils import DateUtil


class DashboardServiceImpl(DashboardService):
    def __init__(
        self,
        dashboard_mapper: DashboardMapper,
        budget_service: BudgetService,
        transaction_service: TransactionService,
    ):
        self.dashboard_mapper = dashboard_mapper
        self.budget_service = budget_service
        self.transaction_service = transaction_service

    def get_dashboard_details(self) -> DashboardDto:
        total_income = (
            self.transaction_service.get_transaction_sum_by_transaction_flow_type(
                TransactionFlow.INCOME
            )
        )
        total_expenses = (
            self.transaction_service.get_transaction_sum_by_transaction_flow_type(
                TransactionFlow.EXPENSE
            )
        )
        current_balance = total_income - total_expenses
        savings_progress = (
            (current_balance / total_income * 100) if total_income else 0.0
        )

        category_spending = self.transaction_service.get_transaction_sum_by_category()
        spent_by_category = dict(category_spending)

        budget_overview = []
        for budget in self.budget_service.get_budget_list_by_month(
            DateUtil.get_current_month_name()
        ):
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
