from datetime import date
from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field

from ...utils import DateUtil


def _future(v: date) -> date:
    if v <= DateUtil.get_today_date():
        raise ValueError("must be a future date")
    return v


FutureDate = Annotated[date, AfterValidator(_future)]


class SavingsGoalCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    target_amount: int = Field(gt=0)
    target_date: FutureDate | None = None
    icon: str | None = Field(default=None, max_length=50)
    color: str | None = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")
