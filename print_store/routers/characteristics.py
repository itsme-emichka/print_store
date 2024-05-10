from fastapi import APIRouter

from models.pattern import Category, Color, StoreSection
from extra.services import (
    get_list_of_objects,
    get_instance_or_404,
    create_instance
)
from schemas.patterns import CategorySchema, ColorSchema, SectionSchema


router = APIRouter()


@router.post('/category')
async def create_category(body: CategorySchema) -> CategorySchema:
    return await create_instance(Category, **body.dict())


@router.get('/category')
async def list_category() -> list[CategorySchema]:
    return await get_list_of_objects(Category)


@router.get('/category/{category_id}')
async def get_category(category_id: int) -> CategorySchema:
    return await get_instance_or_404(Category, id=category_id)


@router.post('/colour')
async def create_colour(body: ColorSchema) -> ColorSchema:
    return await create_instance(Color, **body.dict())


@router.get('/colour')
async def list_colour() -> list[ColorSchema]:
    return await get_list_of_objects(Color)


@router.get('/colour/{category_id}')
async def get_colour(category_id: int) -> ColorSchema:
    return await get_instance_or_404(Color, id=category_id)


@router.post('/section')
async def create_section(body: SectionSchema) -> SectionSchema:
    return await create_instance(StoreSection, **body.dict())


@router.get('/section')
async def list_section() -> list[SectionSchema]:
    return await get_list_of_objects(StoreSection)


@router.get('/section/{category_id}')
async def get_section(category_id: int) -> SectionSchema:
    return await get_instance_or_404(StoreSection, id=category_id)
