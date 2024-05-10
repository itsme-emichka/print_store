from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "storesection" ADD "slug" VARCHAR(256) NOT NULL UNIQUE;
        CREATE UNIQUE INDEX "uid_storesectio_slug_d24bc7" ON "storesection" ("slug");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_storesectio_slug_d24bc7";
        ALTER TABLE "storesection" DROP COLUMN "slug";"""
