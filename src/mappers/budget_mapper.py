from ..models import Budget
from ..routers.dto import BudgetDto
from ..schemas import requests, responses


class BudgetMapper:
    def to_dto_from_create_request(
        self, req: requests.BudgetCreateRequest, user_id: str
    ) -> BudgetDto:
        return BudgetDto(
            user_id=user_id,
            category=req.category,
            amount=req.amount,
        )

    def to_resp(self, dto: BudgetDto) -> responses.BudgetUpsertResponse:
        return responses.BudgetUpsertResponse(
            id=dto.id,
            category=dto.category,
            amount=dto.amount,
        )

    def to_dto_from_edit_request(
        self, req: requests.BudgetEditRequest, user_id: str
    ) -> BudgetDto:
        return BudgetDto(
            amount=req.amount,
            user_id=user_id,
        )

    def to_entity(self, dto: BudgetDto, month: str | None = None) -> Budget:
        return Budget(
            id=dto.id,  # type: ignore
            user_id=dto.user_id,
            amount=dto.amount,
            category=dto.category,
            created_month=month,
        )

    def to_dto_from_entity(self, entity: Budget) -> BudgetDto:
        return BudgetDto(
            id=entity.id,
            user_id=entity.user_id,
            amount=entity.amount,
            category=entity.category,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
            created_month=entity.created_month,
        )
