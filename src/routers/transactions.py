from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas import requests, responses
from ..database import get_db
from ..services import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=responses.TransactionResponse)
def create_transaction(txn: requests.TransactionUpsertRequest, db: Session = Depends(get_db)):
    return TransactionService.create_transaction(db, txn)


@router.get("/", response_model=list[responses.TransactionResponse])
def list_transactions(db: Session = Depends(get_db)):
    return TransactionService.list_transactions(db)
