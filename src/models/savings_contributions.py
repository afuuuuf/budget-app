from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    String,
    func,
)

from ..database import Base
from ..utils import UuidUtil


class SavingsContribution(Base):
    __tablename__ = "savings_contributions"

    id = Column(String, primary_key=True, default=UuidUtil.uuid_v7)
    goal_id = Column(
        String, ForeignKey("savings_goals.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(BigInteger, nullable=False)
    contributed_at = Column(Date, nullable=False)
    note = Column(String(255))
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        CheckConstraint("amount <> 0", name="amount_nonzero"),
        Index("ix_contrib_goal_date", "goal_id", "contributed_at"),
    )
