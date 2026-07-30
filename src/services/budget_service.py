from ..routers.dto import BudgetDto
from ..mappers import BudgetMapper
from ..repository import BudgetRepository

class BudgetService:

    def __init__(self, budget_repo: BudgetRepository, budget_mapper: BudgetMapper):
        self.budget_repo = budget_repo
        self.budget_mapper = budget_mapper

    def create_budget(self, budgetDto: BudgetDto) -> BudgetDto:
        budgetEntity = self.budget_mapper.to_entity(budgetDto)
        created_budget = self.budget_repo.save(budgetEntity)
        return self.budget_mapper.to_dto_from_entity(created_budget)