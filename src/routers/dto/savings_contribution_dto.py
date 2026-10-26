from dataclasses import dataclass
from datetime import date, datetime

from ...enums import SavingGoalStatus


@dataclass
class SavingsContributionDto:
    goal_id: str
    user_id: str
    amount: int
    id: str | None = None
    contributed_at: date | None = None
    contributed_by: str | None = None
    note: str | None = None
    created_at: datetime | None = None
    # status of the goal after this contribution
    last_status: SavingGoalStatus | None = None
