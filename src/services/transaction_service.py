from sqlalchemy.orm import Session

from .. import models
from ..schemas import requests
from ..enums import Category

class TransactionService:
    """Transaction Service Layer"""

    def create_transaction(db: Session, txn: requests.TransactionUpsertRequest) -> models.Transaction:
        db_txn = models.Transaction(**txn.dict())
        db.add(db_txn)
        db.commit()
        db.refresh(db_txn)
        return db_txn


    def list_transactions(db: Session) -> list[models.Transaction]:
        return db.query(models.Transaction).all()
