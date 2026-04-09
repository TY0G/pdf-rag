from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.repositories.user_repo import UserRepository
from app.services.code_service import CodeService


class AuthService:
    def __init__(self, db: Session) -> None:
        self.repo = UserRepository(db)
        self.code_service = CodeService(self.repo)

    def send_code(self, email: str) -> str:
        return self.code_service.send_code(email)

    def register(self, *, email: str, code: str, password: str, nickname: str):
        if self.repo.get_by_email(email):
            raise HTTPException(status_code=400, detail="邮箱已注册")
        if not self.code_service.verify_code(email, code):
            raise HTTPException(status_code=400, detail="验证码无效或已过期")

        user = self.repo.create_user(
            email=email,
            password_hash=get_password_hash(password),
            nickname=nickname,
        )
        token = create_access_token(user.email)
        return token, user

    def login(self, *, email: str, password: str):
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=400, detail="邮箱或密码错误")
        if not user.is_active:
            raise HTTPException(status_code=403, detail="账号已被禁用")
        token = create_access_token(user.email)
        return token, user
