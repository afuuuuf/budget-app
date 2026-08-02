from ..schemas import requests, responses
from ..routers.dto import BudgetDto
from ..models import Budget

class BudgetMapper:
    def to_dto(self, req: requests.BudgetUpsertRequest) -> BudgetDto:
        return BudgetDto(
            budgetType=req.budgetType,
            amount=req.amount,
        )

    
    def to_resp(self, dto: BudgetDto) -> responses.BudgetUpsertResponse:
        return responses.BudgetUpsertResponse(
            id=dto.id,
            budgetType=dto.budgetType,
            amount=dto.amount,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

        # --- Dto -> Repo ---
    def to_entity(self, dto: BudgetDto) -> Budget:
        return Budget(
            id=dto.id, #type: ignore
            amount=dto.amount,
            budgetType= dto.budgetType,
        )

    def to_dto_from_entity(self, entity: Budget) -> BudgetDto:
        return BudgetDto(
            id=entity.id,
            amount=entity.amount,
            budgetType=entity.budgetType,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at
        )

    def update_entity_from_dto(self, entity: Budget, dto: BudgetDto) -> None:
        entity.amount = dto.amount
        entity.budgetType = dto.budgetType