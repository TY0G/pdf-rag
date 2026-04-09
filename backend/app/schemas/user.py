from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserProfile(BaseModel):
    id: int
    email: EmailStr
    nickname: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
