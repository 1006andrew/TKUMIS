# src/api/auth/schemas.py
from pydantic import BaseModel, EmailStr, Field

class RegisterIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)

class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)

class AuthOut(BaseModel):
    ok: bool
    message: str
    redirect: str | None = None
