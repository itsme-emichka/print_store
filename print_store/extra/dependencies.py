from typing import Annotated

from fastapi import Header
from jose import jwt, JWTError

from config import TOKEN_TYPE, SECRET_KEY, ALGORITHM
from extra.http_exceptions import AuthError
from extra.services import get_instance_or_404
from models.users import User


async def is_authenticated(Authorization: Annotated[str, Header()]) -> User:
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
