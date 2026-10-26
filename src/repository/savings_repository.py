from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import SavingsContribution, SavingsGoal
from ..utils import DateUtil


class SavingsRepository:
    def __init__(self, db: Session):
        self.db = db

    # --- Goals: write ---
    def save_goal(self, entity: SavingsGoal) -> SavingsGoal:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update_goal(self, entity: SavingsGoal) -> SavingsGoal:
        entity.updated_at = DateUtil.get_current_time()
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete_goal(self, entity: SavingsGoal) -> SavingsGoal:
        entity.deleted_at = DateUtil.get_current_time()
        self.db.commit()
        self.db.refresh(entity)
        return entity

    # --- Goals: read ---
    def list_goals_for_user(self, user_id: str) -> list[SavingsGoal]:
        return (
            self.db.query(SavingsGoal).filter_by(user_id=user_id, deleted_at=None).all()
        )

    def find_goal_by_id(self, goal_id: str) -> SavingsGoal | None:
        return self.db.query(SavingsGoal).filter_by(id=goal_id, deleted_at=None).first()

    def find_goal_by_id_for_user(
        self, goal_id: str, user_id: str
    ) -> SavingsGoal | None:
        return (
            self.db.query(SavingsGoal)
            .filter_by(id=goal_id, user_id=user_id, deleted_at=None)
            .first()
        )

    def sum_contributions_for_goal(self, goal_id: str) -> int:
        return (
            self.db.query(func.coalesce(func.sum(SavingsContribution.amount), 0))
            .filter(SavingsContribution.goal_id == goal_id)
            .scalar()
        )

    # --- Contributions: write ---
    def save_contribution(self, entity: SavingsContribution) -> SavingsContribution:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update_contribution(self, entity: SavingsContribution) -> SavingsContribution:
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete_contribution(self, entity: SavingsContribution) -> SavingsContribution:
        self.db.delete(entity)
        self.db.commit()
        return entity

    # --- Contributions: read ---
    def list_contributions_for_goal(self, goal_id: str) -> list[SavingsContribution]:
        return (
            self.db.query(SavingsContribution)
            .filter_by(goal_id=goal_id)
            .order_by(SavingsContribution.contributed_at.desc())
            .all()
        )

    def find_contribution_by_id(self, id: str) -> SavingsContribution | None:
        return self.db.query(SavingsContribution).filter_by(id=id).first()
