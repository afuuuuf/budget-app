from ..schemas import requests, responses
from ..routers.dto import TransactionDto
from ..models import Transaction

class TransactionMapper:

    # --- Routers -> Dto Mapper ---
    def to_dto(self, req: requests.TransactionUpsertRequest) -> TransactionDto:
        return TransactionDto(
            amount=req.amount,
            description=req.description,
            category=req.category,
        )

    def to_resp(self, dto: TransactionDto) -> responses.TransactionUpsertResponse:
        return responses.TransactionUpsertResponse(
            id=dto.id,
            amount=dto.amount,
            description=dto.description,
            category=dto.category,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    # --- Dto -> Repo ---
    def to_entity(self, dto: TransactionDto) -> Transaction:
        return Transaction(
            id=dto.id, #type: ignore
            amount=dto.amount,
            description= dto.description,
            category=dto.category,
        )

    def to_dto_from_entity(self, entity: Transaction) -> TransactionDto:
        return TransactionDto(
            id=entity.id,
            amount=entity.amount,
            description=entity.description,
            category=entity.category,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at
        )