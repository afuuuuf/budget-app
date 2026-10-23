from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..mappers import BudgetMapper
from ..repository import BudgetRepository
from ..services import BudgetService
from ..services.impl import BudgetServiceImpl

router = APIRouter(prefix="/savings", tags=["savings"])


def get_mapper() -> BudgetMapper:
    return BudgetMapper()


def get_service(
    db: Session = Depends(get_db),
    mapper: BudgetMapper = Depends(get_mapper),
) -> BudgetService:
    return BudgetServiceImpl(budget_repo=BudgetRepository(db), budget_mapper=mapper)
