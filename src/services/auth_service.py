from ..enums import TokenType
from ..exception import UnauthorizedException, UnsupportedActionException
from ..models import User
from ..repository import UserRepository
from ..schemas import responses
from ..utils import JwtUtil, PasswordUtil


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, email: str, password: str) -> responses.AuthResponse:
        if self.user_repo.find_by_email(email) is not None:
            raise UnsupportedActionException("Email already registered.")
        user = User(email=email, password_hash=PasswordUtil.hash_password(password))
        saved = self.user_repo.save(user)
        return self._issue_tokens(saved.id)

    def login(self, email: str, password: str) -> responses.AuthResponse:
        user = self.user_repo.find_by_email(email)
        if user is None or not PasswordUtil.verify_password(
            password, user.password_hash
        ):
            raise UnauthorizedException("Invalid email or password.")
        return self._issue_tokens(user.id)

    def refresh(self, refresh_token: str) -> responses.AuthResponse:
        payload = JwtUtil.decode_token(refresh_token)
        if payload.get("type") != TokenType.REFRESH:
            raise UnauthorizedException("Refresh token required.")
        user = self.user_repo.find_by_id(payload["sub"])
        if user is None:
            raise UnauthorizedException("User no longer exists.")
        return self._issue_tokens(user.id)

    def _issue_tokens(self, user_id: str) -> responses.AuthResponse:
        return responses.AuthResponse(
            access_token=JwtUtil.create_token(user_id, TokenType.ACCESS),
            refresh_token=JwtUtil.create_token(user_id, TokenType.REFRESH),
        )
