from sqlalchemy.orm import Session

from ..models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, entity: User) -> User:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def find_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter_by(email=email).first()

    def find_by_id(self, id: str) -> User | None:
        return self.db.query(User).filter_by(id=id).first()
