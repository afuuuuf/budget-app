from pydantic import BaseModel

from ...enums import BudgetType


class BudgetCreateRequest(BaseModel):
    budgetType: BudgetType
    amount: float
