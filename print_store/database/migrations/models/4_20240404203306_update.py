from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "patternvariation" ADD "parent_pattern_id" BIGINT NOT NULL;
        ALTER TABLE "patternvariation" ADD CONSTRAINT "fk_patternv_pattern_d39a1fda" FOREIGN KEY ("parent_pattern_id") REFERENCES "pattern" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "patternvariation" DROP CONSTRAINT "fk_patternv_pattern_d39a1fda";
        ALTER TABLE "patternvariation" DROP COLUMN "parent_pattern_id";"""
