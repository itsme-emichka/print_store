from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pattern" ADD "cover" VARCHAR(2048);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pattern" DROP COLUMN "cover";"""
