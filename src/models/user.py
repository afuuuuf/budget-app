from sqlalchemy import Column, DateTime, String

from ..database import Base
from ..utils import DateUtil, UuidUtil


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=UuidUtil.uuid_v7)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=DateUtil.get_current_time, nullable=False)
    updated_at = Column(DateTime, default=DateUtil.get_current_time)
