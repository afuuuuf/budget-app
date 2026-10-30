from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from ..enums import Category, TransactionFlow
from ..utils import DateUtil, UuidUtil


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=UuidUtil.uuid_v7)
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    description: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[Category] = mapped_column(
        Enum(Category, native_enum=False, length=20), index=True, nullable=False
    )
    transaction_flow: Mapped[TransactionFlow] = mapped_column(
        Enum(TransactionFlow, native_enum=False, length=20), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=DateUtil.get_current_time, nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=DateUtil.get_current_time
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
