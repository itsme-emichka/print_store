from datetime import timedelta

from fastapi import APIRouter
import bcrypt

from models.users import User
from schemas.users import PyUserModelIn, TokenOut
from extra.utils import create_access_token
from extra.services import get_instance_or_404
from extra.http_exceptions import WrongPasswordError
from config import ACCESS_TOKEN_EXPIRE_DAYS


router = APIRouter()


@router.post('/login')
async def login(user_data: PyUserModelIn) -> TokenOut:
    user = await get_instance_or_404(
        User,
        username=user_data.username,
        email=user_data.email
    )

    if not bcrypt.checkpw(
        user_data.password.encode(),
        user.hash_password.encode()
    ):
        raise WrongPasswordError
    token = create_access_token(
        data={'sub': user_data.username},
        expires_delta=timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS),
    )
    return TokenOut(token=token)
