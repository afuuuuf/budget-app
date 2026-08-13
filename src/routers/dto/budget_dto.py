from dataclasses import dataclass
from datetime import datetime

from ...enums import BudgetType


@dataclass
class BudgetDto:
    amount: float
    budget_type: BudgetType | None = None
    id: str | None = None
    created_at: datetime | None = None
    created_month: str | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
