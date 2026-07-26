from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel

from ...enums import Category

class TransactionDto(BaseModel):
    id: str | None = None
    amount: Decimal
    description: str | None
    category: Category
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None