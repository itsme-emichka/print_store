from fastapi import APIRouter, Request, HTTPException, status

from models.pattern import (
    Pattern,
    Category,
    PatternVariation
)
from extra.services import (
    create_instance,
    get_parent_pattern,
    create_variation,
    get_instance_or_404,
)
from extra.utils import save_image_from_base64
from schemas.patterns import (
    GetPatternSchema,
    CreatePatternSchema,
    CategorySchema,
    PatternVariationSchema,
    PatternVariationCreationSchema,
    ListPatternSchema,
)


router = APIRouter(prefix='/pattern')


@router.post('/')
async def create_pattern(
    body: CreatePatternSchema,
    request: Request
) -> GetPatternSchema:
    categories_by_slug = await Category.get_categories_by_slug()
    category = categories_by_slug.get(body.category, None)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found'
        )

    parent_pattern = await create_instance(
        Pattern,
        name=body.name,
        slug=body.slug,
        article=body.article,
        description=body.description,
        horizontal_rapport=body.horizontal_rapport,
        vertical_rapport=body.vertical_rapport,
        cover=save_image_from_base64(body.cover, request.base_url),
        price=body.price,
        category=category,
    )

    variations = []

    for variation_data in body.variations:
        variations.append(
            await create_variation(
                parent_pattern.id,
                variation_data.colors,
                variation_data.images,
                request.base_url,
            )
        )

    return GetPatternSchema(
        id=parent_pattern.id,
        name=parent_pattern.name,
        slug=parent_pattern.slug,
        article=parent_pattern.article,
        description=parent_pattern.description,
        horizontal_rapport=parent_pattern.horizontal_rapport,
        vertical_rapport=parent_pattern.vertical_rapport,
        price=parent_pattern.price,
        category=CategorySchema.from_orm(category),
        variations=variations
    )


@router.get('/')
async def get_list_of_patterns() -> list[ListPatternSchema]:
    return await Pattern.all().select_related('category')


@router.get('/{pattern_id}')
async def get_pattern(pattern_id: int) -> GetPatternSchema:
    parent_pattern = await get_parent_pattern(pattern_id)
    variations = []
    for variation in parent_pattern.vars:
        variations.append(PatternVariationSchema(
            id=variation.id,
            colors=await variation.colors,
            images=await variation.images)
        )

    return GetPatternSchema(
            id=parent_pattern.id,
            name=parent_pattern.name,
            slug=parent_pattern.slug,
            article=parent_pattern.article,
            description=parent_pattern.description,
            horizontal_rapport=parent_pattern.horizontal_rapport,
            vertical_rapport=parent_pattern.vertical_rapport,
            price=parent_pattern.price,
            category=CategorySchema.from_orm(parent_pattern.category),
            variations=variations
    )


@router.post('/{pattern_id}/variation/')
async def add_variation(
    pattern_id: int,
    body: PatternVariationCreationSchema,
    request: Request
) -> PatternVariationSchema:
    return await create_variation(
        pattern_id,
        body.colors,
        body.images,
        request.base_url,
    )


@router.get('/{pattern_id}/variation/')
async def get_pattern_variation_list(
    pattern_id: int
) -> list[PatternVariationSchema]:
    parent_pattern = await get_parent_pattern(pattern_id)
    variations = []
    for variation in parent_pattern.vars:
        variations.append(PatternVariationSchema(
            id=variation.id,
            colors=await variation.colors,
            images=await variation.images)
        )
    return variations


@router.get('/{pattern_id}/variation/{pattern_variation_id}/')
async def get_pattern_variation(
    pattern_id: int,
    pattern_variation_id: int,
) -> PatternVariationSchema:
    variation = await get_instance_or_404(
        PatternVariation,
        id=pattern_variation_id,
    )
    return PatternVariationSchema(
        id=variation.id,
        colors=await variation.colors,
        images=await variation.images
    )
