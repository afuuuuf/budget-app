from pydantic import BaseModel
from ...enums import BudgetType

class BudgetDetailsResponse(BaseModel):
    budgetType: BudgetType
    amount: float