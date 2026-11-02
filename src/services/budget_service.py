from ..enums import Category
from ..exception import NotFoundException, UnsupportedActionException
from ..mappers import BudgetMapper
from ..models import Budget
from ..repository import BudgetRepository
from ..routers.dto import BudgetDto
from ..utils import DateUtil

DUPLICATED_BUDGET_ERROR_MSG = "Budget for category {} in {} already exists."
BUDGET_NOT_FOUND_MSG = "Budget for category {} in {} not found."


class BudgetService:
    def __init__(self, budget_repo: BudgetRepository, budget_mapper: BudgetMapper):
        self.budget_repo = budget_repo
        self.budget_mapper = budget_mapper

    def create_budget(self, budget_dto: BudgetDto) -> BudgetDto:
        month = DateUtil.get_current_month_name()

        if budget_dto.category is not None:
            existing_budget_entity = (
                self.budget_repo.find_by_category_and_month_and_user_id(
                    budget_dto.category, month, budget_dto.user_id
                )
            )
            if existing_budget_entity is not None:
                raise UnsupportedActionException(
                    DUPLICATED_BUDGET_ERROR_MSG.format(
                        existing_budget_entity.category,
                        existing_budget_entity.created_month,
                    )
                )
        budget_entity = self.budget_mapper.to_entity(budget_dto, month)
        created_budget = self.budget_repo.save(budget_entity)
        return self.budget_mapper.to_dto_from_entity(created_budget)

    def edit_budget(
        self, budget_dto: BudgetDto, category: Category, month: str
    ) -> BudgetDto:
        budget_entity = self._get_budget_entity_by_category_and_month_and_user_id(
            category, month, budget_dto.user_id
        )
        budget_entity.amount = budget_dto.amount
        edited_budget = self.budget_repo.update(budget_entity)
        return self.budget_mapper.to_dto_from_entity(edited_budget)

    def get_budget_details(
        self, category: Category, month: str, user_id: str
    ) -> BudgetDto:
        budget_entity = self._get_budget_entity_by_category_and_month_and_user_id(
            category, month, user_id
        )
        budgetDto = self.budget_mapper.to_dto_from_entity(budget_entity)
        return budgetDto

    def get_budget_list_by_month(self, month: str, user_id: str) -> list[BudgetDto]:
        budget_entities = self.budget_repo.find_budget_by_month(month, user_id)
        return [
            self.budget_mapper.to_dto_from_entity(budget_entity)
            for budget_entity in budget_entities
        ]

    def _get_budget_entity_by_category_and_month_and_user_id(
        self,
        category: Category,
        month: str,
        user_id: str,
    ) -> Budget:
        budget_entity = self.budget_repo.find_by_category_and_month_and_user_id(
            category, month, user_id
        )
        if not budget_entity:
            raise NotFoundException(BUDGET_NOT_FOUND_MSG.format(category, month))
        return budget_entity
