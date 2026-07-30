from sqlalchemy.orm import Session
from ..models import Transaction
from ..utils import DateUtil

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, entity: Transaction) -> Transaction:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def list_all(self) -> list[Transaction]:
        return self.db.query(Transaction).all()

    def find_by_id(self, id: str) -> Transaction | None:
        return self.db.query(Transaction).filter_by(id = id, deleted_at= None).first()

    def delete(self, entity: Transaction) -> None:
        entity.deleted_at = DateUtil.get_current_time
        self.db.commit()
        self.db.refresh(entity)
        return entity