from fastapi import APIRouter

from models.pattern import Category
from extra.services import (
    get_list_of_objects,
    get_instance_or_404,
    create_instance
)
from schemas.category import CreateCategorySchema, GetCategorySchema


router = APIRouter(prefix='/category')


@router.post('/')
async def create_category(body: CreateCategorySchema) -> GetCategorySchema:
    return await create_instance(Category, **body.dict())


@router.get('/')
async def get_category_list() -> list[GetCategorySchema]:
    return await get_list_of_objects(Category)


@router.get('/{category_id}')
async def get_pattern(category_id: int) -> GetCategorySchema:
    return await get_instance_or_404(Category, id=category_id)
