from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from ..enums import SavingGoalStatus
from ..utils import UuidUtil


class SavingsGoal(Base):
    __tablename__ = "savings_goals"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=UuidUtil.uuid_v7)
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    target_amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    target_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[SavingGoalStatus] = mapped_column(
        Enum(SavingGoalStatus, native_enum=False, length=20),
        nullable=False,
        server_default=SavingGoalStatus.ACTIVE.value,
    )
    icon: Mapped[str | None] = mapped_column(String(50))
    color: Mapped[str | None] = mapped_column(String(7))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint("target_amount > 0", name="target_positive"),
        Index(
            "ix_savings_goals_user",
            "user_id",
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )
