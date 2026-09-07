from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..enums import Status
from ..mappers import TransactionMapper
from ..repository.transaction_repository import TransactionRepository
from ..schemas import requests, responses
from ..services import TransactionService
from ..services.impl import TransactionServiceImpl

router = APIRouter(prefix="/transactions", tags=["transactions"])


def get_mapper() -> TransactionMapper:
    return TransactionMapper()


def get_service(db: Session = Depends(get_db)) -> TransactionService:
    return TransactionServiceImpl(
        transaction_repo=TransactionRepository(db),
        transaction_mapper=TransactionMapper(),
    )


@router.post("", response_model=responses.TransactionUpsertResponse, status_code=201)
def create_transaction(
    txn: requests.TransactionUpsertRequest,
    service: TransactionService = Depends(get_service),
    mapper: TransactionMapper = Depends(get_mapper),
):
    txnDto = mapper.to_dto(txn)
    result = service.create_transaction(txnDto)
    return mapper.to_resp(result)


@router.get("", response_model=list[responses.TransactionUpsertResponse])
def list_transactions(
    service: TransactionService = Depends(get_service),
    mapper: TransactionMapper = Depends(get_mapper),
):
    results = service.list_transactions()
    return [mapper.to_resp(result) for result in results]


@router.get("/{id}", response_model=responses.TransactionUpsertResponse)
def get_transaction(
    id: str,
    service: TransactionService = Depends(get_service),
    mapper: TransactionMapper = Depends(get_mapper),
):
    result = service.get_transaction(id)
    return mapper.to_resp(result)


@router.delete("/{id}", response_model=responses.TransactionStatusResponse)
def delete_transaction(
    id: str,
    service: TransactionService = Depends(get_service),
    mapper: TransactionMapper = Depends(get_mapper),
):
    service.delete_transaction(id)
    return responses.TransactionStatusResponse.get_status_message(Status.DELETED)
