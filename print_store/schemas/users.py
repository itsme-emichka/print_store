from pydantic import BaseModel, EmailStr


class PyUserModelIn(BaseModel):
    username: str
    email: EmailStr
    password: str


class PyUserModeOut(BaseModel):
    username: str
    email: EmailStr
    is_superuser: bool
    is_active: bool


class TokenOut(BaseModel):
    token: str
