from datetime import datetime

from pydantic import BaseModel

from ...enums import Category, TransactionFlow


class TransactionDto(BaseModel):
    id: str | None = None
    user_id: str
    amount: float
    description: str | None
    category: Category
    transaction_flow: TransactionFlow
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
