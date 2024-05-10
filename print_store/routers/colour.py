from fastapi import APIRouter

from models.pattern import Color
from extra.services import (
    get_list_of_objects,
    get_instance_or_404,
    create_instance
)
from schemas.colour import CreateColourSchema, GetColourSchema


router = APIRouter(prefix='/colour')


@router.post('/')
async def create_colour(body: CreateColourSchema) -> GetColourSchema:
    return await create_instance(Color, **body.dict())


@router.get('/')
async def get_category_list() -> list[GetColourSchema]:
    return await get_list_of_objects(Color)


@router.get('/{category_id}')
async def get_pattern(category_id: int) -> GetColourSchema:
    return await get_instance_or_404(Color, id=category_id)
