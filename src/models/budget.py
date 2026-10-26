from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from ..utils import DateUtil, UuidUtil


class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=UuidUtil.uuid_v7)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    budget_type: Mapped[str] = mapped_column(String, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=DateUtil.get_current_time, nullable=False
    )
    created_month: Mapped[str] = mapped_column(
        String, default=DateUtil.get_current_month_name
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=DateUtil.get_current_time
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
