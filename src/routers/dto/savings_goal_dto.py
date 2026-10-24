from dataclasses import dataclass
from datetime import date, datetime

from ...enums import SavingGoalStatus


@dataclass
class SavingsGoalDto:
    user_id: str
    name: str
    target_amount: int
    id: str | None = None
    target_date: date | None = None
    status: SavingGoalStatus = SavingGoalStatus.ACTIVE
    icon: str | None = None
    color: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
