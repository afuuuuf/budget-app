from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..services import DashboardService
from ..services.impl import DashboardServiceImpl
from ..mappers import DashboardMapper

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

def get_mapper() -> DashboardMapper:
    return DashboardMapper()

def get_service(db: Session = Depends(get_db)) -> DashboardService:
    return DashboardServiceImpl(
        dashboard_repo=DashboardRepository(db),
        dashboard_mapper=DashboardMapper()
    )