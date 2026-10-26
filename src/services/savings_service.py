from ..mappers import SavingsMapper
from ..repository import SavingsRepository
from ..routers.dto import SavingsGoalComputedDto, SavingsGoalDto
from ..schemas import SavingsGoalEditRequest


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

    def update_savings_goals(
        self, goal_id: str, user_id: str, editReq: SavingsGoalEditRequest
    ) -> SavingsGoalComputedDto:
        entity = self.savings_repo.find_goal_by_id_for_user(goal_id, user_id)
        self.savings_mapper.apply_edit_to_entity(entity, editReq)
        entity = self.savings_repo.update_goal(entity)
        dto = self.savings_mapper.to_goal_dto_from_entity(entity)
        current = self.savings_repo.sum_contributions_for_goal(dto.id or "")
        return self.savings_mapper.compute_progress(dto, current)

    def list_savings_goals(self, user_id: str) -> list[SavingsGoalComputedDto]:
        computed: list[SavingsGoalComputedDto] = []
        for goal_entity in self.savings_repo.list_goals_for_user(user_id):
            dto = self.savings_mapper.to_goal_dto_from_entity(goal_entity)
            current = self.savings_repo.sum_contributions_for_goal(dto.id or "")
            computed.append(self.savings_mapper.compute_progress(dto, current))
        return computed

    def get_savings_goals(self, goal_id: str, user_id: str) -> SavingsGoalComputedDto:
        entity = self.savings_repo.find_goal_by_id_for_user(goal_id, user_id)
        goalDto = self.savings_mapper.to_goal_dto_from_entity(entity)
        current = self.savings_repo.sum_contributions_for_goal(goalDto.id or "")
        return self.savings_mapper.compute_progress(goalDto, current)
