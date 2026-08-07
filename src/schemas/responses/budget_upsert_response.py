from pydantic import BaseModel

from ...enums import BudgetType

class BudgetUpsertResponse(BaseModel):
    id: str
    budgetType: BudgetType
    amount: float
