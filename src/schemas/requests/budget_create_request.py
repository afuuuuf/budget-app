from pydantic import BaseModel

from ...enums import Category


class BudgetCreateRequest(BaseModel):
    category: Category
    amount: int
