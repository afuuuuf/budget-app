from pydantic import BaseModel, Field

from .savings_contribution_create_request import Amount


class SavingsContributionEditRequest(BaseModel):
    amount: Amount | None = None
    note: str | None = Field(default=None, max_length=255)
