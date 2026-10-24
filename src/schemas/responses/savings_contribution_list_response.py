from pydantic import BaseModel

from .savings_contribution_response import SavingsContributionResponse


class SavingsContributionListResponse(BaseModel):
    items: list[SavingsContributionResponse]
