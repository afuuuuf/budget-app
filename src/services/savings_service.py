from ..exception import NotFoundException
from ..mappers import SavingsMapper
from ..models import User
from ..repository import SavingsRepository
from ..routers.dto import (
    SavingsContributionDto,
    SavingsGoalComputedDto,
    SavingsGoalDto,
)
from ..schemas import SavingsContributionCreateRequest, SavingsGoalEditRequest
from ..utils import DateUtil

SAVING_GOAL_NOT_FOUND_MESSAGE = "Saving Goals Not Found"


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

    def create_contribution(
        self, goal_id: str, user: User, req: SavingsContributionCreateRequest
    ) -> tuple[SavingsContributionDto, SavingsGoalComputedDto]:
        user_id = user.id
        goal_entity = self.savings_repo.find_goal_by_id_for_user(goal_id, user_id)
        if not goal_entity:
            raise NotFoundException(SAVING_GOAL_NOT_FOUND_MESSAGE)

        contribution = self.savings_mapper.to_contribution_dto(req, goal_id, user_id)
        contribution.contributed_at = DateUtil.get_today_date()
        contribution.contributed_by = user.email
        saved = self.savings_repo.save_contribution(
            self.savings_mapper.to_contribution_entity(contribution)
        )
        contribution_dto = self.savings_mapper.to_contribution_dto_from_entity(saved)

        goal_dto = self.savings_mapper.to_goal_dto_from_entity(goal_entity)
        current = self.savings_repo.sum_contributions_for_goal(goal_id)
        goal_computed = self.savings_mapper.compute_progress(goal_dto, current)
        return contribution_dto, goal_computed

    def list_contributions(
        self, goal_id: str, user_id: str
    ) -> list[SavingsContributionDto]:
        goal_entity = self.savings_repo.find_goal_by_id_for_user(goal_id, user_id)
        if not goal_entity:
            raise NotFoundException(SAVING_GOAL_NOT_FOUND_MESSAGE)

        contribution_list: list[SavingsContributionDto] = []
        for contribution_entity in self.savings_repo.list_contributions_for_goal(
            goal_id
        ):
            dto = self.savings_mapper.to_contribution_dto_from_entity(
                contribution_entity
            )
            contribution_list.append(dto)
        return contribution_list

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

    def delete_savings_goals(self, goal_id: str, user_id: str) -> SavingsGoalDto | None:
        entity = self.savings_repo.find_goal_by_id_for_user(goal_id, user_id)
        if not entity:
            raise NotFoundException(SAVING_GOAL_NOT_FOUND_MESSAGE)
        dto = self.savings_mapper.to_goal_dto_from_entity(entity)
        self.savings_repo.delete_goal(entity)
        return dto
