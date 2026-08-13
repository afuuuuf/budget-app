from ..models import Budget
from ..routers.dto import BudgetDto
from ..schemas import requests, responses


class BudgetMapper:
    def to_dto_from_create_request(
        self, req: requests.BudgetCreateRequest
    ) -> BudgetDto:
        return BudgetDto(
            budget_type=req.budgetType,
            amount=req.amount,
        )

    def to_resp(self, dto: BudgetDto) -> responses.BudgetUpsertResponse:
        return responses.BudgetUpsertResponse(
            id=dto.id,
            budgetType=dto.budget_type,
            amount=dto.amount,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )

    def to_dto_from_edit_request(self, req: requests.BudgetEditRequest) -> BudgetDto:
        return BudgetDto(
            amount=req.amount,
        )

        # --- Dto -> Repo ---

    def to_entity(self, dto: BudgetDto) -> Budget:
        return Budget(
            id=dto.id,  # type: ignore
            amount=dto.amount,
            budget_type=dto.budget_type,
        )

    def to_dto_from_entity(self, entity: Budget) -> BudgetDto:
        return BudgetDto(
            id=entity.id,
            amount=entity.amount,
            budget_type=entity.budget_type,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
            created_month=entity.created_month,
        )

    def update_entity_from_dto(self, entity: Budget, dto: BudgetDto) -> None:
        entity.amount = dto.amount
        entity.budget_type = dto.budget_type
