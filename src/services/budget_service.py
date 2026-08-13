from abc import ABC, abstractmethod

from ..enums import BudgetType
from ..routers.dto import BudgetDto


class BudgetService(ABC):
    @abstractmethod
    def create_budget(self, budgetDto: BudgetDto) -> BudgetDto: ...

    @abstractmethod
    def edit_budget(
        self, budgetDto: BudgetDto, budgetType: BudgetType, month: str
    ) -> BudgetDto: ...

    @abstractmethod
    def get_budget_details(
        self, budgetType: BudgetType, month: str
    ) -> BudgetDto | None: ...
