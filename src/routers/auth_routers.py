from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import User
from ..repository import UserRepository
from ..schemas import requests, responses
from ..services import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def get_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(user_repo=UserRepository(db))


@router.post("/register", response_model=responses.AuthResponse, status_code=201)
def register_user(
    body: requests.AuthRegisterRequest,
    service: AuthService = Depends(get_service),
):
    result = service.register(body.email, body.password)
    return result


@router.post("/login", response_model=responses.AuthResponse, status_code=200)
def login(
    body: requests.AuthLoginRequest,
    service: AuthService = Depends(get_service),
):
    result = service.login(body.email, body.password)
    return result


@router.post("/refresh", response_model=responses.AuthResponse, status_code=200)
def refresh(
    body: requests.AuthRefreshRequest,
    service: AuthService = Depends(get_service),
):
    result = service.refresh(body.refresh_token)
    return result


@router.post("/logout", status_code=204)
def logout(user: User = Depends(get_current_user)):
    return None


@router.get("/user-info", response_model=responses.UserInfoResponse)
def get_user_info(user: User = Depends(get_current_user)):
    return responses.UserInfoResponse(id=user.id, email=user.email)
