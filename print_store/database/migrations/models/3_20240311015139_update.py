from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ALTER COLUMN "salt" TYPE BYTEA USING "salt"::BYTEA;
        ALTER TABLE "user" ALTER COLUMN "password" TYPE BYTEA USING "password"::BYTEA;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ALTER COLUMN "salt" TYPE VARCHAR(64) USING "salt"::VARCHAR(64);
        ALTER TABLE "user" ALTER COLUMN "password" TYPE VARCHAR(512) USING "password"::VARCHAR(512);"""
