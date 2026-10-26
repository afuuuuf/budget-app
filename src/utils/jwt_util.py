from datetime import UTC, datetime, timedelta
from typing import Any, TypedDict, cast

import jwt
from jwt import InvalidTokenError

from ..config import settings
from ..enums import TokenType
from ..exception import UnauthorizedException

ACCESS_TOKEN_MINUTES = 30
REFRESH_TOKEN_DAYS = 30


class TokenClaims(TypedDict):
    sub: str
    type: str
    iat: int
    exp: int


class JwtUtil:
    @staticmethod
    def create_token(user_id: str, token_type: TokenType) -> str:
        lifetime = (
            timedelta(minutes=ACCESS_TOKEN_MINUTES)
            if token_type == TokenType.ACCESS
            else timedelta(days=REFRESH_TOKEN_DAYS)
        )
        now = datetime.now(UTC)
        payload: dict[str, Any] = {
            "sub": user_id,
            "type": token_type,
            "iat": now,
            "exp": now + lifetime,
        }
        return jwt.encode(  # type: ignore[reportUnknownMemberType]
            payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def decode_token(token: str) -> TokenClaims:
        try:
            return cast(
                TokenClaims,
                jwt.decode(  # type: ignore[reportUnknownMemberType]
                    token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
                ),
            )
        except InvalidTokenError:
            raise UnauthorizedException("Invalid or expired token.") from None
