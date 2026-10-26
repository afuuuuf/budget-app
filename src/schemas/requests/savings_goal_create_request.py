from datetime import date
from typing import Annotated

from pydantic import AfterValidator, BaseModel, BeforeValidator, Field

from ...validator import ColorValidator, DateValidator

FutureDate = Annotated[
    date,
    BeforeValidator(DateValidator.dateIsoFormatValidation),
    AfterValidator(DateValidator.futureDateValidation),
]
HexColor = Annotated[
    str | None, AfterValidator(ColorValidator.hexColorFormatValidation)
]


class SavingsGoalCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    target_amount: int = Field(gt=0)
    target_date: FutureDate | None = None
    icon: str | None = Field(default=None, max_length=50)
    color: HexColor = None
