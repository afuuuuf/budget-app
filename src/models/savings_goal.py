from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    func,
    text,
)

from ..database import Base
from ..enums import SavingGoalStatus
from ..utils import UuidUtil


class SavingsGoal(Base):
    __tablename__ = "savings_goals"

    id = Column(String, primary_key=True, default=UuidUtil.uuid_v7)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    target_amount = Column(BigInteger, nullable=False)
    target_date = Column(Date)
    status = Column(
        Enum(SavingGoalStatus, native_enum=False, length=16),
        nullable=False,
        server_default=SavingGoalStatus.ACTIVE.value,
    )
    icon = Column(String(50))
    color = Column(String(7))
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deleted_at = Column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint("target_amount > 0", name="target_positive"),
        Index(
            "ix_savings_goals_user",
            "user_id",
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )
