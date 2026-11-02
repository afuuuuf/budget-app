from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..enums import Status
from ..mappers import TransactionMapper
from ..models import User
from ..repository.transaction_repository import TransactionRepository
from ..schemas import requests, responses
from ..services import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])


def get_mapper() -> TransactionMapper:
    return TransactionMapper()


def get_service(
    db: Session = Depends(get_db),
    mapper: TransactionMapper = Depends(get_mapper),
) -> TransactionService:
    return TransactionService(
        transaction_repo=TransactionRepository(db),
        transaction_mapper=mapper,
    )


@router.post(
    "",
    response_model=responses.TransactionUpsertResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    transaction: requests.TransactionUpsertRequest,
    user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_service),
    mapper: TransactionMapper = Depends(get_mapper),
):
    transaction_dto = mapper.to_dto(transaction, user.id)
    result = service.create_transaction(transaction_dto)
    return mapper.to_resp(result)


@router.get("", response_model=list[responses.TransactionUpsertResponse])
def list_transactions(
    user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_service),
    mapper: TransactionMapper = Depends(get_mapper),
):
    results = service.list_transactions(user.id)
    return [mapper.to_resp(result) for result in results]


@router.get("/{id}", response_model=responses.TransactionUpsertResponse)
def get_transaction(
    id: str,
    user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_service),
    mapper: TransactionMapper = Depends(get_mapper),
):
    result = service.get_transaction(id, user.id)
    return mapper.to_resp(result)


@router.delete("/{id}", response_model=responses.StatusResponse)
def delete_transaction(
    id: str,
    user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_service),
):
    service.delete_transaction(id, user.id)
    return responses.StatusResponse.get_status_message(Status.DELETED)
