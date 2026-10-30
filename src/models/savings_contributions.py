from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from ..utils import UuidUtil


class SavingsContribution(Base):
    __tablename__ = "savings_contributions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=UuidUtil.uuid_v7)
    goal_id: Mapped[str] = mapped_column(
        String, ForeignKey("savings_goals.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    contributed_at: Mapped[date] = mapped_column(Date, nullable=False)
    contributed_by: Mapped[str | None] = mapped_column(String(255))
    note: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        CheckConstraint("amount <> 0", name="amount_nonzero"),
        Index("ix_contrib_goal_date", "goal_id", "contributed_at"),
    )
