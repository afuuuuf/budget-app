from pydantic import BaseModel

from ...enums import BudgetType

class BudgetUpsertRequest(BaseModel):
    budgetType: BudgetType
    amount: float