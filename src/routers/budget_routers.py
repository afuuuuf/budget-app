from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..enums import BudgetType
from ..mappers import BudgetMapper
from ..models import User
from ..repository import BudgetRepository
from ..schemas import requests, responses
from ..services import BudgetService

router = APIRouter(prefix="/budgets", tags=["budgets"])


def get_mapper() -> BudgetMapper:
    return BudgetMapper()


def get_service(
    db: Session = Depends(get_db),
    mapper: BudgetMapper = Depends(get_mapper),
) -> BudgetService:
    return BudgetService(budget_repo=BudgetRepository(db), budget_mapper=mapper)


@router.post("", response_model=responses.BudgetUpsertResponse, status_code=201)
def create_budget(
    budget: requests.BudgetCreateRequest,
    user: User = Depends(get_current_user),
    budget_service: BudgetService = Depends(get_service),
    mapper: BudgetMapper = Depends(get_mapper),
):
    budget_dto = mapper.to_dto_from_create_request(budget, user.id)
    result = budget_service.create_budget(budget_dto)
    return mapper.to_resp(result)


@router.put("", response_model=responses.BudgetUpsertResponse, status_code=200)
def edit_budget(
    budget: requests.BudgetEditRequest,
    user: User = Depends(get_current_user),
    budgetType: BudgetType = Query(..., description="Filter by budget type"),
    month: str = Query(..., description="Filter by Month"),
    budget_service: BudgetService = Depends(get_service),
    mapper: BudgetMapper = Depends(get_mapper),
):
    budget_dto = mapper.to_dto_from_edit_request(budget, user.id)
    result = budget_service.edit_budget(budget_dto, budgetType, month)
    return mapper.to_resp(result)


@router.get("", response_model=responses.BudgetDetailsResponse)
def get_budget_details(
    user: User = Depends(get_current_user),
    budgetType: BudgetType = Query(..., description="Filter by budget type"),
    month: str = Query(..., description="Filter by Month"),
    budget_service: BudgetService = Depends(get_service),
    mapper: BudgetMapper = Depends(get_mapper),
):
    result = budget_service.get_budget_details(budgetType, month, user.id)
    return mapper.to_resp(result)
