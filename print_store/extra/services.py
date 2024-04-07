from tortoise.models import Model
from tortoise.queryset import QuerySet, QuerySetSingle
from tortoise.exceptions import IntegrityError

from extra.http_exceptions import Error404, AlreadyExistsError
from extra.utils import get_password_hash
from models.users import User


async def create_instance(model: Model, **kwargs) -> QuerySetSingle:
    try:
        return await model.create(**kwargs)
    except IntegrityError:
        raise AlreadyExistsError


async def get_instance_or_404(model: Model, **kwargs) -> QuerySetSingle:
    instance = await model.get_or_none(**kwargs)
    if not instance:
        raise Error404
    return instance


async def get_instance(model: Model, **kwargs) -> QuerySetSingle:
    return await model.get_or_none(**kwargs)


async def get_list_of_objects(model: Model) -> QuerySet:
    return await model.all()


async def create_user(
    username: str,
    email: str,
    password: str,
    is_superuser: bool = False,
    is_active: bool = True
) -> User:
    hash_pass = get_password_hash(password)
    return await create_instance(
        User,
        username=username,
        email=email,
        hash_password=hash_pass.decode(),
        is_superuser=is_superuser,
        is_active=is_active,
    )
