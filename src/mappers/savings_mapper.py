from ..models import SavingsContribution, SavingsGoal
from ..routers.dto import (
    SavingsContributionDto,
    SavingsGoalComputedDto,
    SavingsGoalDto,
)
from ..schemas import requests, responses
from ..utils import DateUtil

MONTHS_PER_YEAR = 12


class SavingsMapper:
    # --- Routers -> Dto ---
    def to_goal_dto(
        self, req: requests.SavingsGoalCreateRequest, user_id: str
    ) -> SavingsGoalDto:
        return SavingsGoalDto(
            user_id=user_id,
            name=req.name,
            target_amount=req.target_amount,
            target_date=req.target_date,
            icon=req.icon,
            color=req.color,
        )

    def to_contribution_dto(
        self,
        req: requests.SavingsContributionCreateRequest,
        goal_id: str,
        user_id: str,
    ) -> SavingsContributionDto:
        return SavingsContributionDto(
            goal_id=goal_id,
            user_id=user_id,
            amount=req.amount,
            contributed_at=req.contributed_at or DateUtil.get_today_date(),
            note=req.note,
        )

    # --- Dto <-> Entity ---
    def to_goal_entity(self, dto: SavingsGoalDto) -> SavingsGoal:
        return SavingsGoal(
            id=dto.id,  # type: ignore
            name=dto.name,
            user_id=dto.user_id,
            target_amount=dto.target_amount,
            target_date=dto.target_date,
            status=dto.status,
            icon=dto.icon,
            color=dto.color,
        )

    def to_goal_dto_from_entity(self, entity: SavingsGoal) -> SavingsGoalDto:
        return SavingsGoalDto(
            id=entity.id,
            user_id=entity.user_id,
            name=entity.name,
            target_amount=entity.target_amount,
            target_date=entity.target_date,
            status=entity.status,
            icon=entity.icon,
            color=entity.color,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    def to_contribution_entity(
        self, dto: SavingsContributionDto
    ) -> SavingsContribution:
        return SavingsContribution(
            id=dto.id,  # type: ignore
            goal_id=dto.goal_id,
            user_id=dto.user_id,
            amount=dto.amount,
            contributed_at=dto.contributed_at,
            note=dto.note,
        )

    def to_contribution_dto_from_entity(
        self, entity: SavingsContribution
    ) -> SavingsContributionDto:
        return SavingsContributionDto(
            id=entity.id,
            goal_id=entity.goal_id,
            user_id=entity.user_id,
            amount=entity.amount,
            contributed_at=entity.contributed_at,
            note=entity.note,
            created_at=entity.created_at,
        )

    # --- Computed fields (pure math; current_amount supplied by the repo/service) ---
    @staticmethod
    def compute_progress(
        dto: SavingsGoalDto, current_amount: int | None
    ) -> SavingsGoalComputedDto:
        remaining = (
            dto.target_amount - current_amount if current_amount is not None else None
        )
        percent = (
            round(current_amount / dto.target_amount * 100, 2)
            if current_amount is not None
            else None
        )

        monthly_needed: int | None = None
        on_track: bool | None = None
        if remaining is not None and dto.target_date is not None:
            months_left = max(
                1,
                (dto.target_date.year - DateUtil.get_today_date().year) * 12
                + (dto.target_date.month - DateUtil.get_today_date().month),
            )
            monthly_needed = max(0, round(remaining / months_left))

        return SavingsGoalComputedDto(
            user_id=dto.user_id,
            name=dto.name,
            target_amount=dto.target_amount,
            id=dto.id,
            target_date=dto.target_date,
            status=dto.status,
            icon=dto.icon,
            color=dto.color,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            deleted_at=dto.deleted_at,
            current_amount=current_amount,
            remaining_amount=remaining,
            percent_complete=percent,
            monthly_needed=monthly_needed,
            on_track=on_track,
        )

    # --- Dto -> Responses ---
    def to_goal_resp(
        self, dto: SavingsGoalComputedDto
    ) -> responses.SavingsGoalResponse:
        return responses.SavingsGoalResponse(
            id=dto.id,
            name=dto.name,
            target_amount=dto.target_amount,
            current_amount=dto.current_amount,
            remaining_amount=dto.remaining_amount,
            percent_complete=dto.percent_complete,
            target_date=dto.target_date,
            monthly_needed=dto.monthly_needed,
            on_track=dto.on_track,
            status=dto.status,
            icon=dto.icon,
            color=dto.color,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )

    def to_contribution_resp(
        self, dto: SavingsContributionDto
    ) -> responses.SavingsContributionResponse:
        return responses.SavingsContributionResponse(
            id=dto.id,
            goal_id=dto.goal_id,
            amount=dto.amount,
            contributed_at=dto.contributed_at,
            note=dto.note,
            created_at=dto.created_at,
        )

    def to_contribution_result_resp(
        self,
        contribution: SavingsContributionDto,
        goal: SavingsGoalComputedDto,
    ) -> responses.SavingsContributionResultResponse:
        return responses.SavingsContributionResultResponse(
            contribution=self.to_contribution_resp(contribution),
            goal=self.to_goal_resp(goal),
        )

    def to_goal_list_resp(
        self, goals: list[SavingsGoalComputedDto]
    ) -> responses.SavingsGoalListResponse:
        return responses.SavingsGoalListResponse(
            items=[self.to_goal_resp(g) for g in goals]
        )

    def to_contribution_list_resp(
        self, contributions: list[SavingsContributionDto]
    ) -> responses.SavingsContributionListResponse:
        return responses.SavingsContributionListResponse(
            items=[self.to_contribution_resp(c) for c in contributions]
        )
