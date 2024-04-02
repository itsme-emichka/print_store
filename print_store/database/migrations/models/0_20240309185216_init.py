from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "category" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(512) NOT NULL UNIQUE,
    "slug" VARCHAR(256) NOT NULL UNIQUE
);
COMMENT ON COLUMN "category"."name" IS 'Название категории принта';
COMMENT ON COLUMN "category"."slug" IS 'Слаг категории принта';
CREATE TABLE IF NOT EXISTS "color" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(512) NOT NULL UNIQUE,
    "slug" VARCHAR(256) NOT NULL UNIQUE,
    "hex" VARCHAR(7) NOT NULL
);
COMMENT ON COLUMN "color"."name" IS 'Название цвета';
COMMENT ON COLUMN "color"."slug" IS 'Слаг цвета';
CREATE TABLE IF NOT EXISTS "image" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(512) NOT NULL UNIQUE,
    "image_url" VARCHAR(1024) NOT NULL,
    "is_main" BOOL NOT NULL  DEFAULT False
);
COMMENT ON COLUMN "image"."name" IS 'Название цвета';
CREATE TABLE IF NOT EXISTS "pattern" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(512)  UNIQUE,
    "slug" VARCHAR(256)  UNIQUE,
    "price" DECIMAL(16,2) NOT NULL,
    "category_id" BIGINT REFERENCES "category" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "pattern"."name" IS 'Название принта';
COMMENT ON COLUMN "pattern"."slug" IS 'Слаг принта';
COMMENT ON COLUMN "pattern"."price" IS 'Цена принта';
COMMENT ON COLUMN "pattern"."category_id" IS 'Категория принта';
CREATE TABLE IF NOT EXISTS "patternvariation" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS "patterncolor" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "color_id" BIGINT NOT NULL REFERENCES "color" ("id") ON DELETE CASCADE,
    "pattern_id" BIGINT NOT NULL REFERENCES "patternvariation" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "patternimage" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "image_id" BIGINT NOT NULL REFERENCES "image" ("id") ON DELETE CASCADE,
    "pattern_id" BIGINT NOT NULL REFERENCES "patternvariation" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "PatternImage" (
    "patternvariation_id" BIGINT NOT NULL REFERENCES "patternvariation" ("id") ON DELETE SET NULL,
    "image_id" BIGINT NOT NULL REFERENCES "image" ("id") ON DELETE SET NULL
);
COMMENT ON TABLE "PatternImage" IS 'Картинки паттерна в определенном цвете';
CREATE TABLE IF NOT EXISTS "PatternColor" (
    "patternvariation_id" BIGINT NOT NULL REFERENCES "patternvariation" ("id") ON DELETE CASCADE,
    "color_id" BIGINT NOT NULL REFERENCES "color" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "PatternColor" IS 'Образец паттерна в определенном цвете';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
