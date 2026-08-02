from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import requests, responses
from ..services import BudgetService
from ..repository import BudgetRepository
from ..mappers import BudgetMapper

router = APIRouter(prefix="/budgets", tags=["budgets"])

def get_mapper() -> BudgetMapper:
    return BudgetMapper()

def get_service(db: Session = Depends(get_db)) -> BudgetService:
    return BudgetService(
        budget_repo=BudgetRepository(db),
        budget_mapper=BudgetMapper()
    )

class BudgetRouters:

    @router.post("/", response_model=responses.BudgetUpsertResponse, status_code=201)
    def create_budget(budget: requests.BudgetUpsertRequest, budget_service: BudgetService = Depends(get_service), mapper: BudgetMapper = Depends(get_mapper)):
        budgetDto = mapper.to_dto(budget)
        result = budget_service.create_budget(budgetDto)
        return mapper.to_resp(result)

    @router.put("/{id}", response_model=responses.BudgetUpsertResponse, status_code=200)
    def edit_budget(id: str, budget: requests.BudgetUpsertRequest, budget_service: BudgetService = Depends(get_service), mapper: BudgetMapper = Depends(get_mapper)):
        budgetDto = mapper.to_dto(budget)
        result = budget_service.edit_budget(id, budgetDto)
        return mapper.to_resp(result)