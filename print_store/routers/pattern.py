from fastapi import APIRouter, Request, HTTPException, status

from models.pattern import (
    Pattern,
    Category,
    StoreSection
)
from extra.services import (
    create_instance,
    get_parent_pattern,
    create_variation,
    get_pattern_variation as get_pattern_variation_db,
)
from extra.utils import (
    save_image_from_base64,
    get_final_article_of_pattern_var
)
from extra.http_exceptions import Error404
from schemas.patterns import (
    GetPatternSchema,
    CreatePatternSchema,
    CategorySchema,
    PatternVariationSchema,
    PatternVariationCreationSchema,
    ListPatternSchema,
    SectionSchema,
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

    sections_by_slug = await StoreSection.get_sections_by_slug()
    section = sections_by_slug.get(body.section, None)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Section not found'
        )

    parent_pattern = await create_instance(
        Pattern,
        section=section,
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
                variation_data.number_of_variation
            )
        )

    return GetPatternSchema(
        id=parent_pattern.id,
        name=parent_pattern.name,
        section=SectionSchema.from_orm(section),
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
    return await Pattern.all(
    ).select_related(
        'category'
    ).select_related(
        'section'
    )


@router.get('/{pattern_id}')
async def get_pattern(pattern_id: int) -> GetPatternSchema:
    parent_pattern = await get_parent_pattern(pattern_id)
    variations = []
    for variation in parent_pattern.vars:
        final_article = get_final_article_of_pattern_var(
            parent_pattern.article,
            variation.number_of_variation,
            parent_pattern.section.article_marker,
        )
        variations.append(PatternVariationSchema(
            id=variation.id,
            final_article=final_article,
            number_of_variation=variation.number_of_variation,
            colors=await variation.colors,
            images=await variation.images)
        )

    return GetPatternSchema(
        id=parent_pattern.id,
        name=parent_pattern.name,
        slug=parent_pattern.slug,
        section=SectionSchema.from_orm(parent_pattern.section),
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
        final_article = get_final_article_of_pattern_var(
            parent_pattern.article,
            variation.number_of_variation,
            parent_pattern.section.article_marker,
        )
        variations.append(PatternVariationSchema(
            id=variation.id,
            final_article=final_article,
            number_of_variation=variation.number_of_variation,
            colors=await variation.colors,
            images=await variation.images)
        )
    return variations


@router.get('/{pattern_id}/variation/{pattern_variation_id}/')
async def get_pattern_variation(
    pattern_id: int,
    pattern_variation_id: int,
) -> PatternVariationSchema:
    variation = await get_pattern_variation_db(pattern_variation_id)
    final_article = get_final_article_of_pattern_var(
        variation.parent_pattern.article,
        variation.number_of_variation,
        variation.parent_pattern.section.article_marker
    )
    return PatternVariationSchema(
        id=variation.id,
        final_article=final_article,
        number_of_variation=variation.number_of_variation,
        colors=await variation.colors,
        images=await variation.images
    )


@router.post(
    '/{pattern_id}/variation/{pattern_variation_id}/cart/'
)
async def add_pattern_variation_to_cart(
    request: Request,
    pattern_id: int,
    pattern_variation_id: int,
    amount: int = 1
):
    cart = request.session.get('cart', None)
    if not cart:
        request.session['cart'] = dict()
        cart = request.session.get('cart', None)

    pattern_in_cart: dict[str, int] = cart.get(str(pattern_variation_id), None)
    pattern = await get_pattern_variation(
        pattern_id, pattern_variation_id
    )
    if not pattern_in_cart:
        cart[pattern_variation_id] = {
            'pattern_variation_id': pattern_variation_id,
            'parent_pattern_id': pattern_id,
            'final_article': pattern.final_article,
            'amount': amount
        }
    else:
        pattern_in_cart['amount'] = pattern_in_cart.get('amount') + amount

    return request.session.get('cart')


@router.delete(
    '/{pattern_id}/variation/{pattern_variation_id}/cart/'
)
async def delete_pattern_variation_from_cart(
    request: Request,
    pattern_id: int,
    pattern_variation_id: int,
    amount: int | str = 1
):
    try:
        cart: dict[str, int] = request.session['cart']
        pattern_in_cart: dict[str, int] = cart[str(pattern_variation_id)]
    except KeyError:
        raise Error404

    if amount == 'all':
        request.session.pop('cart')
        return

    if isinstance(amount, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'Wrong amount': "int or 'all' are available"}
        )

    final_amount = pattern_in_cart.get('amount') - amount
    if final_amount <= 0:
        cart.pop(str(pattern_variation_id))
    pattern_in_cart['amount'] = final_amount

    return request.session.get('cart')
