from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from ..database import Base
from ..utils import UuidUtil


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=UuidUtil.uuid_v7)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)