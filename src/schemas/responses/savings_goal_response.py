from datetime import date, datetime

from pydantic import BaseModel

from ...enums import SavingGoalStatus


class SavingsGoalResponse(BaseModel):
    id: str
    name: str
    target_amount: int
    current_amount: int
    remaining_amount: int
    percent_complete: float
    target_date: date | None
    monthly_needed: int | None
    on_track: bool | None
    status: SavingGoalStatus
    icon: str | None
    color: str | None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
