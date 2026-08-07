from sqlalchemy import Column, String, Float, DateTime
from ..database import Base
from ..utils import UuidUtil, DateUtil

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=UuidUtil.uuid_v7)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, index=True)
    created_at = Column(DateTime, default=DateUtil.get_current_time)
    updated_at = Column(DateTime, default=DateUtil.get_current_time)
    deleted_at = Column(DateTime, nullable=True)