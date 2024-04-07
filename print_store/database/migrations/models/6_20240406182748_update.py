from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "hash_password" VARCHAR(256) NOT NULL;
        ALTER TABLE "user" DROP COLUMN "salt";
        ALTER TABLE "user" DROP COLUMN "password";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "salt" BYTEA NOT NULL;
        ALTER TABLE "user" ADD "password" BYTEA NOT NULL;
        ALTER TABLE "user" DROP COLUMN "hash_password";"""
