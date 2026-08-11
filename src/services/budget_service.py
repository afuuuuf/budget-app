from ..routers.dto import BudgetDto
from ..mappers import BudgetMapper
from ..repository import BudgetRepository
from ..enums import BudgetType
from ..exception import NotFoundException, UnsupportedActionException
from ..utils import DateUtil

DUPLICATED_BUDGET_ERROR_MSG = "Budget for budget type {} in {} already exists."
BUDGET_NOT_FOUND_MSG = "Budget for budget type {} in {} not found."

class BudgetService:

    def __init__(self, budget_repo: BudgetRepository, budget_mapper: BudgetMapper):
        self.budget_repo = budget_repo
        self.budget_mapper = budget_mapper

    def create_budget(self, budgetDto: BudgetDto) -> BudgetDto:
        existingBudgetEntity = self.budget_repo.find_by_budget_type_and_month(budgetDto.budget_type, DateUtil.get_current_month_name())
        if existingBudgetEntity is not None:
            raise UnsupportedActionException(DUPLICATED_BUDGET_ERROR_MSG.format(existingBudgetEntity.budget_type, existingBudgetEntity.created_month))
        budgetEntity = self.budget_mapper.to_entity(budgetDto)
        created_budget = self.budget_repo.save(budgetEntity)
        return self.budget_mapper.to_dto_from_entity(created_budget)

    def edit_budget(self, budgetDto: BudgetDto, budgetType: BudgetType, month: str) -> BudgetDto:
        budgetEntity = self.budget_repo.find_by_budget_type_and_month(budgetType, month)
        if budgetEntity is None:
            raise NotFoundException(BUDGET_NOT_FOUND_MSG.format(budgetType, month))
        newDto = self.budget_mapper.to_dto_from_entity(budgetEntity)
        newDto.amount = budgetDto.amount
        self.budget_mapper.update_entity_from_dto(budgetEntity, newDto)
        edited_budget = self.budget_repo.update(budgetEntity)
        return self.budget_mapper.to_dto_from_entity(edited_budget)

    def get_budget_details(self, budgetType: BudgetType, month: str) -> BudgetDto | None:
        budgetEntity = self.budget_repo.find_by_budget_type_and_month(budgetType, month)
        if not budgetEntity:
            raise NotFoundException(BUDGET_NOT_FOUND_MSG.format(budgetType, month))
        budgetDto = self.budget_mapper.to_dto_from_entity(budgetEntity)
        return budgetDto