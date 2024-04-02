from pydantic import BaseModel, EmailStr


class PyUserModelIn(BaseModel):
    username: str
    email: EmailStr
    password: str


class PyUserModeOut(BaseModel):
    username: str
    email: EmailStr


class TokenOut(BaseModel):
    token: str
