from typing import Annotated

from pydantic import BaseModel
from fastapi import Query

from config import SLUG_PATTERN, HEX_PATTERN
from schemas.abstract import AbstractId


class CreateColourSchema(BaseModel):
    name: str
    slug: Annotated[str, Query(pattern=SLUG_PATTERN)]
    hex: Annotated[str, Query(pattern=HEX_PATTERN)]


class GetColourSchema(CreateColourSchema, AbstractId):
    pass
