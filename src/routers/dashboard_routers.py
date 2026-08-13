from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..mappers import DashboardMapper
from ..schemas import responses, requests
from ..services import DashboardService
from ..services.impl import DashboardServiceImpl
from ..repository import TransactionRepository, BudgetRepository

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def get_mapper() -> DashboardMapper:
    return DashboardMapper()


def get_service(db: Session = Depends(get_db)) -> DashboardService:
    return DashboardServiceImpl(
        transaction_repo=TransactionRepository(db),
        budget_repo=BudgetRepository(db),
        dashboard_mapper=DashboardMapper()
    )

class DashboardRouters:
    @router.get("", response_model=responses.DashboardListResponse, status_code=200)
    def get_dashboard_list(
        service: DashboardService = Depends(get_service),
        mapper: DashboardMapper = Depends(get_mapper),
    ):
        result = service.get_dashboard_details()
        return mapper.to_resp(result)
