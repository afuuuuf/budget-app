from datetime import date
from typing import Annotated

from pydantic import AfterValidator, BaseModel, BeforeValidator, Field

from ...validator import AmountValidator, DateValidator

PastOrToday = Annotated[
    date,
    BeforeValidator(DateValidator.dateIsoFormatValidation),
    AfterValidator(DateValidator.notFutureDateValidation),
]


class SavingsContributionCreateRequest(BaseModel):
    amount: AmountValidator
    contributed_at: PastOrToday | None = None
    note: str | None = Field(default=None, max_length=255)
