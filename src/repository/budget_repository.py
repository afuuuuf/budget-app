from datetime import datetime

from sqlalchemy.orm import Session
from ..models import Budget

class BudgetRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, entity: Budget) -> Budget:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def list_all(self) -> list[Budget]:
        return self.db.query(Budget).all()

    def find_by_id(self, id: str) -> Budget | None:
        return self.db.query(Budget).filter_by(id = id, deleted_at= None).first()

    def delete(self, entity: Budget) -> None:
        entity.deleted_at = datetime.now()
        self.db.commit()
        self.db.refresh(entity)
        return entity