from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..mappers import BudgetMapper, DashboardMapper, TransactionMapper
from ..repository import BudgetRepository, TransactionRepository
from ..schemas import responses
from ..services import BudgetService, DashboardService, TransactionService
from ..services.impl import DashboardServiceImpl, TransactionServiceImpl

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def get_mapper() -> DashboardMapper:
    return DashboardMapper()


def get_budget_mapper() -> BudgetMapper:
    return BudgetMapper()


def get_transaction_mapper() -> TransactionMapper:
    return TransactionMapper()


def get_budget_service(
    db: Session = Depends(get_db),
    budget_mapper: BudgetMapper = Depends(get_budget_mapper),
) -> BudgetService:
    return BudgetService(budget_repo=BudgetRepository(db), budget_mapper=budget_mapper)


def get_transaction_service(
    db: Session = Depends(get_db),
    transaction_mapper: TransactionMapper = Depends(get_transaction_mapper),
) -> TransactionService:
    return TransactionServiceImpl(
        transaction_repo=TransactionRepository(db),
        transaction_mapper=transaction_mapper,
    )


def get_service(
    db: Session = Depends(get_db),
    mapper: DashboardMapper = Depends(get_mapper),
    budget_service: BudgetService = Depends(get_budget_service),
    transaction_service: TransactionService = Depends(get_transaction_service),
) -> DashboardService:
    return DashboardServiceImpl(
        dashboard_mapper=mapper,
        budget_service=budget_service,
        transaction_service=transaction_service,
    )


@router.get("", response_model=responses.DashboardListResponse, status_code=200)
def get_dashboard_list(
    service: DashboardService = Depends(get_service),
    mapper: DashboardMapper = Depends(get_mapper),
):
    result = service.get_dashboard_details()
    return mapper.to_resp(result)
