from pydantic import BaseModel

from ...enums import Category


class BudgetDetailsResponse(BaseModel):
    category: Category
    amount: int
