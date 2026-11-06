from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from ..enums import Category, Month
from ..utils import DateUtil, UuidUtil


class Budget(Base):
    __tablename__ = "budgets"

    __table_args__ = (
    Index(
        "ix_budgets_user_month", "user_id", "created_month",
        postgresql_where=text("deleted_at IS NULL"),
    ),
)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=UuidUtil.uuid_v7)
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    category: Mapped[Category] = mapped_column(
        Enum(Category, native_enum=False, length=20),
        index=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=DateUtil.get_current_time, nullable=False
    )
    created_month: Mapped[Month] = mapped_column(
        Enum(Month, native_enum=False, length=20),
        default=DateUtil.get_current_month,
        nullable=False,
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=DateUtil.get_current_time
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
