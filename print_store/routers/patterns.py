from fastapi import APIRouter, Request

from models.pattern import (
    Pattern,
    PatternVariation,
    Color,
    PatternColor,
    PatternImage,
    Category,
    Image
)
from extra.services import (
    get_list_of_objects,
    get_instance_or_404,
    create_instance
)
from extra.utils import save_image_from_base64
from schemas.patterns import GetPatternSchema, CreatePatternSchema, CategorySchema, PatternVariationSchema


router = APIRouter(prefix='/pattern')


@router.get('/{pattern_id}')
async def get_pattern(pattern_id: int) -> GetPatternSchema:
    parent_pattern = await Pattern.all().select_related('category').get(id=pattern_id)
    category = parent_pattern.category
    variations = await PatternVariation.filter(parent_pattern=parent_pattern)
    vas = []
    for variation in variations:
        colors = await Color.filter(pattern_color__pattern=variation)
        images = await Image.filter(pattern_image__pattern=variation)
        vas.append(PatternVariationSchema(colors=colors, images=images))

    return GetPatternSchema(
            id=parent_pattern.id,
            name=parent_pattern.name,
            slug=parent_pattern.slug,
            price=parent_pattern.price,
            category=CategorySchema.from_orm(category),
            variations=vas
    )



@router.post('/')
async def create_pattern(body: CreatePatternSchema, request: Request) -> GetPatternSchema:
    category = await get_instance_or_404(Category, slug=body.category)

    parent_pattern = await create_instance(
        Pattern,
        name=body.name,
        slug=body.slug,
        price=body.price,
        category=category,
    )

    all_colors = await get_list_of_objects(Color)
    colors_by_slug = dict()
    for color in all_colors:
        colors_by_slug[str(color.slug)] = color

    variations = []

    for variation_data in body.variations:
        variation = await create_instance(
            PatternVariation, parent_pattern=parent_pattern)

        pattern_colors = []
        colors_list = []

        pattern_images = []
        images_list = []

        for color_data in variation_data.colors:
            color = colors_by_slug.get(color_data.slug, None)
            if not color:
                print(f'Цвета {color_data.slug} нет в базе данных')
                continue
            pattern_colors.append(PatternColor(pattern=variation, color=color))
            colors_list.append(color)

        for image_data in variation_data.images:
            img = await create_instance(
                Image,
                image_url=save_image_from_base64(
                    image_data.base_64,
                    request.base_url
                ),
                is_main=image_data.is_main
            )
            pattern_images.append(PatternImage(pattern=variation, image=img))
            images_list.append(img)

        await PatternColor.bulk_create(pattern_colors)
        await PatternImage.bulk_create(pattern_images)

        variations.append({'colors': colors_list, 'images': images_list})

    return {
        'id': parent_pattern.id,
        'name': parent_pattern.name,
        'slug': parent_pattern.slug,
        'price': parent_pattern.price,
        'category': category,
        'variations': variations
    }


@router.get('/{pattern_id}')
async def get_pattern(pattern_id: int) -> GetPatternSchema:
    return await get_instance_or_404(Pattern, id=pattern_id)
