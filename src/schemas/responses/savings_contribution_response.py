from datetime import date, datetime

from pydantic import BaseModel


class SavingsContributionResponse(BaseModel):
    id: str
    goal_id: str
    amount: int
    contributed_at: date
    contributed_by: str
    note: str | None
    created_at: datetime | None = None

    class Config:
        from_attributes = True
