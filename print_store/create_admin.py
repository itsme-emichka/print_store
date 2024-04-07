from tortoise import Tortoise, run_async

from database.db import TORTOISE_ORM
from extra.services import create_user


async def create_admin(
    username: str,
    email: str,
    password: str,
    is_superuser: bool = True,
    is_active: bool = True
):
    await Tortoise.init(TORTOISE_ORM)
    await create_user(username, email, password, is_superuser, is_active)
    return


if __name__ == '__main__':
    username = input('username:')
    email = input('email:')
    password = input('password:')
    run_async(create_admin(username, email, password))
