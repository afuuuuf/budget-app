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

    def _flow_filters(self, flow: TransactionFlow) -> list[ColumnElement[bool]]:
        return [
            Transaction.transaction_flow == flow,
            Transaction.deleted_at.is_(None),
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

    def find_by_flow(self, flow: TransactionFlow) -> list[Transaction]:
        return self.db.query(Transaction).filter(*self._flow_filters(flow)).all()

    def delete(self, entity: Transaction) -> None:
        entity.deleted_at = DateUtil.get_current_time()
        self.db.commit()
        self.db.refresh(entity)

    def sum_by_flow(self, flow: TransactionFlow) -> float:
        return (
            self.db.query(func.coalesce(func.sum(Transaction.amount), 0.0))
            .filter(*self._flow_filters(flow))
            .scalar()
        )

    def sum_by_category(self) -> list[tuple[str, float]]:
        rows = (
            self.db.query(Transaction.category, func.sum(Transaction.amount))
            .filter(*self._flow_filters(TransactionFlow.EXPENSE))
            .group_by(Transaction.category)
            .all()
        )
        return [(category, amount) for category, amount in rows]
