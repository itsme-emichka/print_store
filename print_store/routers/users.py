from typing import Annotated

from fastapi import APIRouter, Depends
from tortoise.exceptions import IntegrityError

from models.users import User
from schemas.users import PyUserModelIn, PyUserModeOut
from routers import auth
from extra.services import (
    get_instance,
    get_list_of_objects,
    create_user as create_db_user,
)
from extra.http_exceptions import AlreadyExistsError
from extra.dependencies import is_authenticated


router = APIRouter(prefix='/users')
router.include_router(auth.router)


@router.post('/')
async def create_user(user: PyUserModelIn) -> PyUserModeOut:
    if await get_instance(User, username=user.username, email=user.email):
        raise AlreadyExistsError
    try:
        return await create_db_user(
            username=user.username,
            email=user.email,
            password=user.password,
            is_active=True,
        )
    except IntegrityError:
        raise AlreadyExistsError


@router.get('/')
async def get_user_list() -> list[PyUserModeOut]:
    return await get_list_of_objects(User)


@router.get('/me')
async def get_current_user(
    user: Annotated[str, Depends(is_authenticated)],
) -> PyUserModeOut:
    return user
