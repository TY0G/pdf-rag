import random
import string
from datetime import datetime, timedelta, timezone

from app.repositories.user_repo import UserRepository


class CodeService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def send_code(self, email: str) -> str:
        code = "".join(random.choices(string.digits, k=6))
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
        self.repo.save_email_code(email=email, code=code, expires_at=expires_at)
        return code

    def verify_code(self, email: str, code: str) -> bool:
        row = self.repo.get_latest_available_code(email)
        if not row:
            return False
        if row.code != code:
            return False
        if row.expires_at < datetime.now(timezone.utc):
            return False
        self.repo.mark_code_used(row)
        return True
