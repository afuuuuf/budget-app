from pydantic import BaseModel

from ...enums import BudgetType

class BudgetUpsertResponse(BaseModel):
    budgetType: BudgetType
    amount: float
