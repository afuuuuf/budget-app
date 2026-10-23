from datetime import UTC, datetime, timedelta
from typing import Literal

import jwt
from jwt import InvalidTokenError

from ..config import settings
from ..exception import UnauthorizedException

ACCESS_TOKEN_MINUTES = 30
REFRESH_TOKEN_DAYS = 30


class JwtUtil:
    @staticmethod
    def create_token(user_id: str, token_type: Literal["access", "refresh"]) -> str:
        lifetime = (
            timedelta(minutes=ACCESS_TOKEN_MINUTES)
            if token_type == "access"
            else timedelta(days=REFRESH_TOKEN_DAYS)
        )
        now = datetime.now(UTC)
        payload = {
            "sub": user_id,
            "type": token_type,
            "iat": now,
            "exp": now + lifetime,
        }
        return jwt.encode(
            payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(
                token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
            )
        except InvalidTokenError:
            raise UnauthorizedException("Invalid or expired token.") from None
