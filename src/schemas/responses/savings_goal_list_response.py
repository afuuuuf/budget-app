from pydantic import BaseModel

from .savings_goal_response import SavingsGoalResponse


class SavingsGoalListResponse(BaseModel):
    items: list[SavingsGoalResponse]
