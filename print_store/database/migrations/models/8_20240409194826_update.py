from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "PatternImage";
        DROP TABLE IF EXISTS "PatternColor";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE "PatternColor" (
    "color_id" BIGINT NOT NULL REFERENCES "color" ("id") ON DELETE CASCADE,
    "patternvariation_id" BIGINT NOT NULL REFERENCES "patternvariation" ("id") ON DELETE CASCADE
);
        CREATE TABLE "PatternImage" (
    "image_id" BIGINT NOT NULL REFERENCES "image" ("id") ON DELETE CASCADE,
    "patternvariation_id" BIGINT NOT NULL REFERENCES "patternvariation" ("id") ON DELETE CASCADE
);"""
