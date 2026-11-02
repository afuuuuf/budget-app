from sqlalchemy import ColumnElement, func
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

    def _flow_filters(
        self, flow: TransactionFlow, user_id: str
    ) -> list[ColumnElement[bool]]:
        return [
            Transaction.transaction_flow == flow,
            Transaction.deleted_at.is_(None),
            Transaction.user_id == user_id,
        ]

    def list_all(self, user_id: str) -> list[Transaction]:
        return (
            self.db.query(Transaction).filter_by(user_id=user_id, deleted_at=None).all()
        )

    def find_by_id(self, id: str, user_id: str) -> Transaction | None:
        return (
            self.db.query(Transaction)
            .filter_by(id=id, user_id=user_id, deleted_at=None)
            .first()
        )

    def delete(self, entity: Transaction) -> None:
        entity.deleted_at = DateUtil.get_current_time()
        self.db.commit()
        self.db.refresh(entity)

    def sum_by_flow(self, flow: TransactionFlow, user_id: str) -> int:
        return (
            self.db.query(func.coalesce(func.sum(Transaction.amount), 0))
            .filter(*self._flow_filters(flow, user_id))
            .scalar()
        )

    def sum_by_category(self, user_id: str) -> list[tuple[str, int]]:
        rows = (
            self.db.query(Transaction.category, func.sum(Transaction.amount))
            .filter(*self._flow_filters(TransactionFlow.EXPENSE, user_id))
            .group_by(Transaction.category)
            .all()
        )
        return [(category, amount) for category, amount in rows]
