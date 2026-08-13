from sqlalchemy import Column, DateTime, Float, String

from ..database import Base
from ..utils import DateUtil, UuidUtil


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=UuidUtil.uuid_v7)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, index=True, nullable=False)
    transaction_flow = Column(String, nullable=False)
    created_at = Column(DateTime, default=DateUtil.get_current_time, nullable=False)
    updated_at = Column(DateTime, default=DateUtil.get_current_time)
    deleted_at = Column(DateTime, nullable=True)
