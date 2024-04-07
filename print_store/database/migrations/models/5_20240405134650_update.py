from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "is_superuser" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "user" ADD "is_active" BOOL NOT NULL  DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "is_superuser";
        ALTER TABLE "user" DROP COLUMN "is_active";"""
