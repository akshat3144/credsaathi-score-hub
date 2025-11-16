from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    name: str
    picture: Optional[str] = None


class UserCreate(UserBase):
    google_id: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    picture: Optional[str] = None


class UserInDB(UserBase):
    id: str
    google_id: Optional[str] = None
    role: str = "user"
    created_at: datetime
    last_login: datetime
    
    class Config:
        from_attributes = True
