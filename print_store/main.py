from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from fastadmin import fastapi_app as admin_app
from dotenv import load_dotenv

from routers import users, patterns, category
from database.db import TORTOISE_ORM
from config import ALLOWED_ORIGINS


load_dotenv(override=True)


app = FastAPI()

app.include_router(users.router)
app.include_router(patterns.router)
app.include_router(category.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/admin', admin_app)

register_tortoise(
    app,
    TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
