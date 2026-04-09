from pydantic import BaseModel, EmailStr, Field

from app.schemas.user import UserProfile


class SendCodeRequest(BaseModel):
    email: EmailStr


class SendCodeResponse(BaseModel):
    message: str
    dev_code: str | None = None


class RegisterRequest(BaseModel):
    email: EmailStr
    code: str = Field(min_length=4, max_length=12)
    password: str = Field(min_length=6, max_length=128)
    nickname: str = Field(min_length=2, max_length=30)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfile
