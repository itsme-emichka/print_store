from tortoise.models import Model

from extra.http_exceptions import Error404


async def create_instance(model: Model, **kwargs) -> Model:
    return await model.create(**kwargs)


async def get_instance_or_404(model: Model, **kwargs) -> Model:
    instance = await model.get_or_none(**kwargs)
    if not instance:
        raise Error404
    return instance


async def get_instance(model: Model, **kwargs) -> Model:
    return await model.get_or_none(**kwargs)
