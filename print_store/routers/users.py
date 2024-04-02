import os
from typing import Annotated

from fastapi import APIRouter, Depends
from tortoise.exceptions import IntegrityError

from models.users import User
from py_models.users import PyUserModelIn, PyUserModeOut
from extra.utils import get_password_hash
from routers import auth
from extra.http_exceptions import UserAlreadyExistsError
from extra.services import get_instance, create_instance
from dependencies.users import is_authenticated


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
    user: Annotated[str, Depends(is_authenticated)],
) -> PyUserModeOut:
    return user
