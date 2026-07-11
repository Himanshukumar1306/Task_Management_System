
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import RoleEnum

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: RoleEnum = RoleEnum.employee

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(UserBase):
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str
    role: RoleEnum
    user_id: int

