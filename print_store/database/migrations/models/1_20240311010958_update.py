from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(256) NOT NULL UNIQUE,
    "email" VARCHAR(256) NOT NULL UNIQUE,
    "password" VARCHAR(512) NOT NULL,
    "token" VARCHAR(512)
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "user";"""
