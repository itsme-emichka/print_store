from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from routers import users
from database.db import TORTOISE_ORM


app = FastAPI()

app.include_router(users.router)

register_tortoise(
    app,
    TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
