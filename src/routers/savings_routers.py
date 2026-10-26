from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..mappers import SavingsMapper
from ..models import User
from ..repository import SavingsRepository
from ..schemas import requests, responses
from ..services import SavingsService

router = APIRouter(prefix="/savings", tags=["savings"])


def get_mapper() -> SavingsMapper:
    return SavingsMapper()


def get_service(
    db: Session = Depends(get_db),
    mapper: SavingsMapper = Depends(get_mapper),
) -> SavingsService:
    return SavingsService(savings_repo=SavingsRepository(db), savings_mapper=mapper)


@router.post(
    "",
    response_model=responses.SavingsGoalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_savings_goals(
    svgGoals: requests.SavingsGoalCreateRequest,
    user: User = Depends(get_current_user),
    service: SavingsService = Depends(get_service),
    mapper: SavingsMapper = Depends(get_mapper),
):
    svgGoalDto = mapper.to_goal_dto(svgGoals, user.id)
    result = service.create_savings_goals(svgGoalDto)
    return mapper.to_goal_resp(result)


@router.put("/{id}", response_model=responses.SavingsGoalResponse)
def update_savings_goals(
    id: str,
    svgGoals: requests.SavingsGoalEditRequest,
    user: User = Depends(get_current_user),
    service: SavingsService = Depends(get_service),
    mapper: SavingsMapper = Depends(get_mapper),
):
    result = service.update_savings_goals(id, user.id, svgGoals)
    return mapper.to_goal_resp(result)


@router.get(
    "/{id}",
    response_model=responses.SavingsGoalResponse,
    status_code=status.HTTP_200_OK,
)
def get_savings_goals(
    id: str,
    user: User = Depends(get_current_user),
    service: SavingsService = Depends(get_service),
    mapper: SavingsMapper = Depends(get_mapper),
):
    result = service.get_savings_goals(id, user.id)
    return mapper.to_goal_resp(result)


@router.get(
    "", response_model=responses.SavingsGoalListResponse, status_code=status.HTTP_200_OK
)
def list_savings_goals(
    user: User = Depends(get_current_user),
    service: SavingsService = Depends(get_service),
    mapper: SavingsMapper = Depends(get_mapper),
):
    results = service.list_savings_goals(user.id)
    return mapper.to_goal_list_resp(results)
