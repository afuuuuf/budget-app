from pydantic import BaseModel

from ...enums import Category

class TransactionUpsertRequest(BaseModel):
    description: str
    amount: float
    category: Category