import calendar

from sqlalchemy import Column, String, Float, DateTime
from datetime import datetime
from ..database import Base
from ..utils import UuidUtil, DateUtil

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(String, primary_key=True, default=UuidUtil.uuid_v7)
    amount = Column(Float, nullable=False)
    budgetType = Column(String, index=True)
    created_at = Column(DateTime, default=DateUtil.get_current_time)
    created_month = Column(String, default=DateUtil.get_current_month_name)
    updated_at = Column(DateTime, default=DateUtil.get_current_time)
    deleted_at = Column(DateTime, nullable=True)