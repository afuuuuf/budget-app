from pydantic import BaseModel


class BudgetEditRequest(BaseModel):
    amount: float
