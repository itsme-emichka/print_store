from fastapi import APIRouter

from models.pattern import Pattern
from extra.services import (
    get_list_of_objects,
    get_instance_or_404,
    create_instance
)
from schemas.patterns import GetPatternSchema, CreatePatternSchema


router = APIRouter(prefix='/pattern')


@router.get('/')
async def pattern_list() -> list[GetPatternSchema]:
    return await get_list_of_objects(Pattern)


@router.post('/')
async def create_pattern(body: CreatePatternSchema) -> GetPatternSchema:
    return await create_instance(Pattern, **body)


@router.get('/{pattern_id}')
async def get_pattern(pattern_id: int) -> GetPatternSchema:
    return await get_instance_or_404(Pattern, id=pattern_id)
