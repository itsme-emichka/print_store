from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "usershoppingcart" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "amount" INT NOT NULL,
    "material_id" BIGINT NOT NULL REFERENCES "material" ("id") ON DELETE CASCADE,
    "pattern_variation_id" BIGINT NOT NULL REFERENCES "patternvariation" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "usershoppingcart"."amount" IS 'Количество товара в корзине';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "usershoppingcart";"""
