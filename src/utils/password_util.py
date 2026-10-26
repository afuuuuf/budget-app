import bcrypt


class PasswordUtil:
    @staticmethod
    def hash_password(plain: str) -> str:
        return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(plain: str, stored: str) -> bool:
        return bcrypt.checkpw(plain.encode(), stored.encode())
