from sqlalchemy import Column, String, Float, DateTime
from ..database import Base
from ..utils import UuidUtil, DateUtil

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(String, primary_key=True, default=UuidUtil.uuid_v7)
    amount = Column(Float, nullable=False)
    budget_type = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=DateUtil.get_current_time, nullable=False)
    created_month = Column(String, default=DateUtil.get_current_month_name)
    updated_at = Column(DateTime, default=DateUtil.get_current_time)
    deleted_at = Column(DateTime, nullable=True)