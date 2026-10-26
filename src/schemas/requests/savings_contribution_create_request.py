from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field

from ...validator import AmountValidator

Amount = Annotated[
    int,
    AfterValidator(AmountValidator.non_zero),
    AfterValidator(AmountValidator.within_limit),
]


class SavingsContributionCreateRequest(BaseModel):
    amount: Amount
    note: str | None = Field(default=None, max_length=255)
