import re
from datetime import date
from typing import Annotated

from pydantic import AfterValidator, BaseModel, BeforeValidator, Field

from ...utils import DateUtil


def _future(v: date) -> date:
    if v <= DateUtil.get_today_date():
        raise ValueError("must be a future date")
    return v


def parse_date_str(v: date | str) -> date:
    """Coerce an ISO date string to date, with a clear format message."""
    if isinstance(v, str):
        try:
            return date.fromisoformat(v.strip())
        except ValueError:
            raise ValueError(
                'must be in "YYYY-MM-DD" format (e.g. 2026-11-25)'
            ) from None
    return v


def _validate_hex_color(v: str | None) -> str | None:
    if v is not None and re.fullmatch(r"#[0-9a-fA-F]{6}", v) is None:
        raise ValueError("must be a hex color in #RRGGBB format (e.g. #ff5733)")
    return v


FutureDate = Annotated[date, BeforeValidator(parse_date_str), AfterValidator(_future)]
HexColor = Annotated[str | None, AfterValidator(_validate_hex_color)]


class SavingsGoalCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    target_amount: int = Field(gt=0)
    target_date: FutureDate | None = None
    icon: str | None = Field(default=None, max_length=50)
    color: HexColor = None
