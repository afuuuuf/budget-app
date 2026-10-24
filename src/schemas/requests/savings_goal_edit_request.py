from pydantic import BaseModel, Field

from ...enums import SavingGoalStatus
from .savings_goal_create_request import FutureDate

_HEX_COLOR_PATTERN = r"^#[0-9a-fA-F]{6}$"


class SavingsGoalEditRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    target_amount: int | None = Field(default=None, gt=0)
    target_date: FutureDate | None = None
    status: SavingGoalStatus | None = None
    icon: str | None = Field(default=None, max_length=50)
    color: str | None = Field(default=None, pattern=_HEX_COLOR_PATTERN)
