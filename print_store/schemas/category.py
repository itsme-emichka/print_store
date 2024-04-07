from typing import Annotated

from pydantic import BaseModel
from fastapi import Query

from config import SLUG_PATTERN
from schemas.abstract import AbstractId


class CreateCategorySchema(BaseModel):
    name: str
    slug: Annotated[str, Query(pattern=SLUG_PATTERN)]


class GetCategorySchema(CreateCategorySchema, AbstractId):
    pass
