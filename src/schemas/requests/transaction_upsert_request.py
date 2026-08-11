from pydantic import BaseModel

from ...enums import Category, TransactionFlow

class TransactionUpsertRequest(BaseModel):
    description: str
    amount: float
    category: Category
    transactionFlow: TransactionFlow