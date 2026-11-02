from enum import StrEnum


class SavingGoalStatus(StrEnum):
    ACTIVE = "ACTIVE"
    ON_HOLD = "ON_HOLD"
    COMPLETED = "COMPLETED"

    def get_status(self, current: int, target_amount: int) -> "SavingGoalStatus":
        if current >= target_amount:
            return SavingGoalStatus.COMPLETED
        if self == SavingGoalStatus.COMPLETED:
            return SavingGoalStatus.ACTIVE
        return self
