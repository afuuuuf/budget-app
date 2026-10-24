from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from ..utils import DateUtil, UuidUtil


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=UuidUtil.uuid_v7)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=DateUtil.get_current_time, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=DateUtil.get_current_time
    )
