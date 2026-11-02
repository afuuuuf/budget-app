from ..enums import TransactionFlow
from ..mappers import DashboardMapper
from ..routers.dto import DashboardDto
from ..utils import DateUtil
from .budget_service import BudgetService
from .transaction_service import TransactionService


class DashboardService:
    def __init__(
        self,
        dashboard_mapper: DashboardMapper,
        budget_service: BudgetService,
        transaction_service: TransactionService,
    ):
        self.dashboard_mapper = dashboard_mapper
        self.budget_service = budget_service
        self.transaction_service = transaction_service

    def get_dashboard_details(self, user_id: str) -> DashboardDto:
        total_income = self.transaction_service.get_transaction_sum_by_transaction_flow_type(
                TransactionFlow.INCOME, user_id
            )
        
        total_expenses = self.transaction_service.get_transaction_sum_by_transaction_flow_type(
                TransactionFlow.EXPENSE, user_id
            )
        
        current_balance = self.transaction_service.get_net_cash_flow(total_income, total_expenses)
        net_savings_rate = self.transaction_service.get_net_savings_rate(total_income, total_expenses)

        category_spending = self.transaction_service.get_transaction_sum_by_category(
            user_id
        )
        spent_by_category = dict(category_spending)

        budget_overview = []
        for budget in self.budget_service.get_budget_list_by_month(
            DateUtil.get_current_month_name(), user_id
        ):
            spent = spent_by_category.get(budget.budget_type, 0)
            budget_overview.append(
                (budget.budget_type, budget.amount, spent, budget.amount - spent)
            )

        return DashboardDto(
            total_income=total_income,
            total_expenses=total_expenses,
            current_balance=current_balance,
            net_savings_rate=net_savings_rate,
            budget_overview=budget_overview,
            category_spending=category_spending,
        )
