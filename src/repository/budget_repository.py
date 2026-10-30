from sqlalchemy.orm import Session

from ..enums import BudgetType
from ..models import Budget
from ..utils import DateUtil


class BudgetRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, entity: Budget) -> Budget:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, entity: Budget) -> Budget:
        entity.updated_at = DateUtil.get_current_time()
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def list_all(self) -> list[Budget]:
        return self.db.query(Budget).all()

    def find_by_id(self, id: str) -> Budget | None:
        return self.db.query(Budget).filter_by(id=id, deleted_at=None).first()

    def find_budget_by_month(self, month: str) -> list[Budget]:
        return (
            self.db.query(Budget).filter_by(created_month=month, deleted_at=None).all()
        )

    def find_by_budget_type_and_month_and_user_id(
        self, budgetType: BudgetType, month: str, user_id: str
    ) -> Budget | None:
        return (
            self.db.query(Budget)
            .filter_by(budget_type=budgetType, created_month=month, user_id=user_id)
            .first()
        )

    def delete(self, entity: Budget) -> None:
        entity.deleted_at = DateUtil.get_current_time()
        self.db.commit()
        self.db.refresh(entity)