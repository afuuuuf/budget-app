from pydantic import BaseModel

from .savings_contribution_response import SavingsContributionResponse
from .savings_goal_response import SavingsGoalResponse


class SavingsContributionResultResponse(BaseModel):
    contribution: SavingsContributionResponse
    goal: SavingsGoalResponse
