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
    "name" VARCHAR(512)  UNIQUE,
    "image_url" VARCHAR(1024) NOT NULL,
    "is_main" BOOL NOT NULL  DEFAULT False
);
COMMENT ON COLUMN "image"."name" IS 'Название цвета';
CREATE TABLE IF NOT EXISTS "material" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(512) NOT NULL UNIQUE,
    "slug" VARCHAR(256) NOT NULL UNIQUE,
    "width" INT NOT NULL,
    "density" INT NOT NULL
);
COMMENT ON COLUMN "material"."name" IS 'Название материала';
COMMENT ON COLUMN "material"."slug" IS 'Слаг материала';
COMMENT ON COLUMN "material"."width" IS 'Ширина материала в мм';
COMMENT ON COLUMN "material"."density" IS 'Плотность материала в г/м^3';
CREATE TABLE IF NOT EXISTS "storesection" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(512) NOT NULL UNIQUE,
    "slug" VARCHAR(256) NOT NULL UNIQUE,
    "article_marker" VARCHAR(8) NOT NULL UNIQUE
);
COMMENT ON COLUMN "storesection"."name" IS 'Название раздела';
COMMENT ON COLUMN "storesection"."slug" IS 'Слаг раздела';
COMMENT ON COLUMN "storesection"."article_marker" IS 'Маркер раздела';
CREATE TABLE IF NOT EXISTS "pattern" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(512)  UNIQUE,
    "article" VARCHAR(64) NOT NULL,
    "slug" VARCHAR(256)  UNIQUE,
    "price" DECIMAL(16,2) NOT NULL,
    "cover" VARCHAR(2048),
    "description" TEXT,
    "horizontal_rapport" DECIMAL(3,1) NOT NULL,
    "vertical_rapport" DECIMAL(3,1) NOT NULL,
    "category_id" BIGINT REFERENCES "category" ("id") ON DELETE SET NULL,
    "section_id" BIGINT NOT NULL REFERENCES "storesection" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "pattern"."name" IS 'Название принта';
COMMENT ON COLUMN "pattern"."article" IS 'Артикул принта';
COMMENT ON COLUMN "pattern"."slug" IS 'Слаг принта';
COMMENT ON COLUMN "pattern"."price" IS 'Цена принта';
COMMENT ON COLUMN "pattern"."cover" IS 'Обложка принта';
COMMENT ON COLUMN "pattern"."horizontal_rapport" IS 'Горизонтальный раппорт в см';
COMMENT ON COLUMN "pattern"."vertical_rapport" IS 'Вертикальный раппорт в см';
COMMENT ON COLUMN "pattern"."category_id" IS 'Категория принта';
CREATE TABLE IF NOT EXISTS "patternvariation" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "number_of_variation" VARCHAR(8) NOT NULL,
    "parent_pattern_id" BIGINT NOT NULL REFERENCES "pattern" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "patternvariation"."number_of_variation" IS 'Номер цветовой вариации';
COMMENT ON COLUMN "patternvariation"."parent_pattern_id" IS 'Родительский паттерн';
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
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
