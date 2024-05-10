from fastapi import APIRouter

from models.pattern import StoreSection
from extra.services import (
    get_list_of_objects,
    get_instance_or_404,
    create_instance
)
from schemas.patterns import CreateSectionSchema, SectionSchema


router = APIRouter(prefix='/section')


@router.post('/')
async def create_colour(body: CreateSectionSchema) -> SectionSchema:
    return await create_instance(StoreSection, **body.dict())


@router.get('/')
async def get_category_list() -> list[SectionSchema]:
    return await get_list_of_objects(StoreSection)


@router.get('/{category_id}')
async def get_pattern(category_id: int) -> SectionSchema:
    return await get_instance_or_404(StoreSection, id=category_id)
