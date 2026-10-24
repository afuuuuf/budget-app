from dataclasses import dataclass

from .savings_goal_dto import SavingsGoalDto


@dataclass
class SavingsGoalComputedDto(SavingsGoalDto):
    """SavingsGoalDto plus metrics derived from contributions and the clock.

    `current_amount` and derived fields are filled by the mapper/service and
    are None until computed.
    """

    current_amount: int | None = None
    remaining_amount: int | None = None
    percent_complete: float | None = None
    monthly_needed: int | None = None
    on_track: bool | None = None
