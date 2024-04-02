import os
from typing import Annotated

from fastapi import APIRouter, Header
from tortoise.exceptions import IntegrityError
from jose import jwt, JWTError

from models.users import User
from py_models.users import PyUserModelIn, PyUserModeOut
from extra.utils import get_password_hash
from config import ALGORITHM, SECRET_KEY, TOKEN_TYPE
from routers import auth
from extra.http_exceptions import AuthError, UserAlreadyExistsError
from extra.services import get_instance_or_404, get_instance, create_instance


router = APIRouter(prefix='/users')
router.include_router(auth.router)


@router.post('/')
async def create_user(user: PyUserModelIn) -> PyUserModeOut:
    if await get_instance(User, username=user.username, email=user.email):
        raise UserAlreadyExistsError
    salt = os.urandom(64)
    hashed_password = get_password_hash(user.password, salt)
    try:
        user_obj = await create_instance(
            User,
            username=user.username,
            email=user.email,
            password=hashed_password,
            salt=salt,
        )
        return user_obj
    except IntegrityError:
        raise UserAlreadyExistsError


@router.get('/me')
async def get_current_user(
    Authorization: Annotated[str, Header()]
) -> PyUserModeOut:
    token_type, token = Authorization.split()
    if not token_type == TOKEN_TYPE:
        raise AuthError
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if not username:
            raise AuthError
    except JWTError:
        raise AuthError
    return await get_instance_or_404(User, username=username)
