from pydantic import BaseModel

from ...enums import Category


class BudgetUpsertResponse(BaseModel):
    id: str
    category: Category
    amount: int
