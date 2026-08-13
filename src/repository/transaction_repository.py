from sqlalchemy import func
from sqlalchemy.orm import Session

from ..enums import TransactionFlow
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
        return self.db.query(Transaction).filter_by(deleted_at=None).all()

    def find_by_id(self, id: str) -> Transaction | None:
        return self.db.query(Transaction).filter_by(id=id, deleted_at=None).first()

    def delete(self, entity: Transaction) -> None:
        entity.deleted_at = DateUtil.get_current_time()
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def sum_by_flow(self, flow: str) -> float:
        return (
            self.db.query(func.coalesce(func.sum(Transaction.amount), 0.0))
            .filter(
                Transaction.transaction_flow == flow,
                Transaction.deleted_at.is_(None),
            )
            .scalar()
        )

    def sum_by_category(self) -> list[tuple[str, float]]:
        return (
            self.db.query(Transaction.category, func.sum(Transaction.amount))
            .filter(
                Transaction.transaction_flow == TransactionFlow.EXPENSE,
                Transaction.deleted_at.is_(None),
            )
            .group_by(Transaction.category)
            .all()
        )
