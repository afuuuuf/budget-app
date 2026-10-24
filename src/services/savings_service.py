from ..mappers import SavingsMapper
from ..repository import SavingsRepository
from ..routers.dto import SavingsGoalComputedDto, SavingsGoalDto


class SavingsService:
    def __init__(self, savings_repo: SavingsRepository, savings_mapper: SavingsMapper):
        self.savings_repo = savings_repo
        self.savings_mapper = savings_mapper

    def create_savings_goals(
        self, svgGoalDto: SavingsGoalDto
    ) -> SavingsGoalComputedDto:
        svgGoalEntity = self.savings_mapper.to_goal_entity(svgGoalDto)
        createdEntity = self.savings_repo.save_goal(svgGoalEntity)
        goalDto = self.savings_mapper.to_goal_dto_from_entity(createdEntity)
        current = self.savings_repo.sum_contributions_for_goal(goalDto.id or "")
        return self.savings_mapper.compute_progress(goalDto, current)
