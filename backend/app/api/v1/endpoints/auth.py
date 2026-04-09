from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import get_current_user, get_db
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    SendCodeRequest,
    SendCodeResponse,
    TokenResponse,
)
from app.schemas.user import UserProfile
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/send-code", response_model=SendCodeResponse)
def send_code(payload: SendCodeRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    code = service.send_code(payload.email)
    return SendCodeResponse(
        message="验证码已生成。开发模式下直接返回验证码。",
        dev_code=code if settings.debug else None,
    )


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    token, user = service.register(
        email=payload.email,
        code=payload.code,
        password=payload.password,
        nickname=payload.nickname,
    )
    return TokenResponse(access_token=token, user=user)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    token, user = service.login(email=payload.email, password=payload.password)
    return TokenResponse(access_token=token, user=user)


@router.get("/me", response_model=UserProfile)
def me(user=Depends(get_current_user)):
    return user
