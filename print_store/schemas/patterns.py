from typing import Annotated

from pydantic import BaseModel
from fastapi import Query

from config import SLUG_PATTERN, HEX_PATTERN, BASE64_PATTERN


# POST

class ImageCreationSchema(BaseModel):
    is_main: bool = False
    base_64: Annotated[str, Query(pattern=BASE64_PATTERN)]


class ColorCreationSchema(BaseModel):
    slug: Annotated[str, Query(pattern=SLUG_PATTERN)]


class PatternVariationCreationSchema(BaseModel):
    number_of_variation: str
    colors: list[ColorCreationSchema]
    images: list[ImageCreationSchema]


class CreatePatternSchema(BaseModel):
    section: Annotated[str, Query(pattern=SLUG_PATTERN)]
    name: str | None = None
    slug: Annotated[str | None, Query(pattern=SLUG_PATTERN)] = None
    article: str
    description: str | None = None
    horizontal_rapport: float
    vertical_rapport: float
    cover: Annotated[str | None, Query(pattern=BASE64_PATTERN)] = None
    category: Annotated[str, Query(pattern=SLUG_PATTERN)]
    price: int
    variations: list[PatternVariationCreationSchema]


class CreateSectionSchema(BaseModel):
    name: str
    slug: Annotated[str, Query(pattern=SLUG_PATTERN)]
    article_marker: str


# GET

class CategorySchema(BaseModel):
    name: str
    slug: Annotated[str, Query(pattern=SLUG_PATTERN)]

    class Config:
        from_attributes = True


class ColorSchema(BaseModel):
    name: str
    slug: Annotated[str, Query(pattern=SLUG_PATTERN)]
    hex: Annotated[str, Query(pattern=HEX_PATTERN)]

    class Config:
        from_attributes = True


class ImageSchema(BaseModel):
    name: str | None = None
    image_url: str
    is_main: bool = False

    class Config:
        from_attributes = True


class PatternVariationSchema(BaseModel):
    id: int
    number_of_variation: str
    final_article: str
    colors: list[ColorSchema]
    images: list[ImageSchema]

    class Config:
        from_attributes = True


class SectionSchema(CreateSectionSchema):
    pass

    class Config:
        from_attributes = True


class GetPatternSchema(BaseModel):
    id: int
    name: str
    section: SectionSchema
    slug: Annotated[str | None, Query(pattern=SLUG_PATTERN)] = None
    article: str
    description: str | None = None
    horizontal_rapport: float
    vertical_rapport: float
    cover: str | None = None
    price: int
    category: CategorySchema
    variations: list[PatternVariationSchema]

    class Config:
        from_attributes = True


class ListPatternSchema(BaseModel):
    id: int
    name: str
    cover: str | None = None
    slug: Annotated[str | None, Query(pattern=SLUG_PATTERN)] = None
    price: int
    category: CategorySchema
    section: SectionSchema

    class Config:
        from_attributes = True
