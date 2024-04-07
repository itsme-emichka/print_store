from typing import Annotated

from pydantic import BaseModel
from fastapi import Query

from config import SLUG_PATTERN
from schemas.abstract import AbstractId


class PatternVariation(BaseModel):
    colors: list[int] | None
    images: list[int] | None


class CreatePatternSchema(BaseModel):
    name: str | None
    slug: Annotated[str, Query(pattern=SLUG_PATTERN)] | None
    category: Annotated[str, Query(pattern=SLUG_PATTERN)]
    price: int
    variations: list[PatternVariation] | None


class GetPatternSchema(CreatePatternSchema, AbstractId):
    pass
