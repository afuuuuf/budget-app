from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..database import get_db
from ..enums import TokenType
from ..exception import UnauthorizedException
from ..models import User
from ..repository import UserRepository
from ..utils import JwtUtil

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = JwtUtil.decode_token(token)
    if payload.get("type") != TokenType.ACCESS:
        raise UnauthorizedException("Access token required.")
    user = UserRepository(db).find_by_id(payload["sub"])
    if user is None:
        raise UnauthorizedException("User no longer exists.")
    return user
