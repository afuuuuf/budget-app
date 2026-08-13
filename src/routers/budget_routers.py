from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..enums import BudgetType
from ..mappers import BudgetMapper
from ..repository import BudgetRepository
from ..schemas import requests, responses
from ..services import BudgetService

router = APIRouter(prefix="/budgets", tags=["budgets"])


def get_mapper() -> BudgetMapper:
    return BudgetMapper()


def get_service(db: Session = Depends(get_db)) -> BudgetService:
    return BudgetService(budget_repo=BudgetRepository(db), budget_mapper=BudgetMapper())


class BudgetRouters:
    @router.post("", response_model=responses.BudgetUpsertResponse, status_code=201)
    def create_budget(
        budget: requests.BudgetCreateRequest,
        budget_service: BudgetService = Depends(get_service),
        mapper: BudgetMapper = Depends(get_mapper),
    ):
        budgetDto = mapper.to_dto_from_create_request(budget)
        result = budget_service.create_budget(budgetDto)
        return mapper.to_resp(result)

    @router.put("", response_model=responses.BudgetUpsertResponse, status_code=200)
    def edit_budget(
        budget: requests.BudgetEditRequest,
        budgetType: BudgetType = Query(..., description="Filter by budget type"),
        month: str = Query(..., description="Filter by Month"),
        budget_service: BudgetService = Depends(get_service),
        mapper: BudgetMapper = Depends(get_mapper),
    ):
        budgetDto = mapper.to_dto_from_edit_request(budget)
        result = budget_service.edit_budget(budgetDto, budgetType, month)
        return mapper.to_resp(result)

    @router.get("", response_model=responses.BudgetDetailsResponse)
    def get_budget_details(
        budgetType: BudgetType = Query(..., description="Filter by budget type"),
        month: str = Query(..., description="Filter by Month"),
        budget_service: BudgetService = Depends(get_service),
        mapper: BudgetMapper = Depends(get_mapper),
    ):
        result = budget_service.get_budget_details(budgetType, month)
        return mapper.to_resp(result)
