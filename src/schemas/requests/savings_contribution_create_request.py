from datetime import date
from typing import Annotated

from pydantic import AfterValidator, BaseModel, BeforeValidator, Field, field_validator

from ...utils import DateUtil
from .savings_goal_create_request import parse_date_str


def _not_future(v: date) -> date:
    if v > DateUtil.get_today_date():
        raise ValueError("cannot be in the future")
    return v


PastOrToday = Annotated[
    date, BeforeValidator(parse_date_str), AfterValidator(_not_future)
]


class SavingsContributionCreateRequest(BaseModel):
    amount: int
    contributed_at: PastOrToday | None = None
    note: str | None = Field(default=None, max_length=255)

    @field_validator("amount")
    @classmethod
    def non_zero(cls, v: int) -> int:
        if v == 0:
            raise ValueError("cannot be 0")
        return v
