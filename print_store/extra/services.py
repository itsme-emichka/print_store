from tortoise.models import Model
from tortoise.queryset import QuerySet, QuerySetSingle
from tortoise.exceptions import IntegrityError
from tortoise.query_utils import Prefetch

from extra.http_exceptions import Error404, AlreadyExistsError
from extra.utils import get_password_hash, save_image_from_base64
from models.users import User
from models.pattern import (
    Pattern,
    PatternVariation,
    Color,
    Image,
    PatternColor,
    PatternImage,
)
from schemas.patterns import (
    ColorCreationSchema,
    ImageCreationSchema,
    PatternVariationSchema
)


async def create_instance(model: Model, **kwargs) -> QuerySetSingle | None:
    try:
        return await model.create(**kwargs)
    except IntegrityError as ex:
        print(ex)
        raise AlreadyExistsError


async def get_instance_or_404(model: Model, **kwargs) -> QuerySetSingle:
    instance = await model.get_or_none(**kwargs)
    if not instance:
        raise Error404
    return instance


async def get_instance(model: Model, **kwargs) -> QuerySetSingle:
    return await model.get_or_none(**kwargs)


async def get_list_of_objects(model: Model, **kwargs) -> QuerySet:
    if not kwargs:
        return await model.all()
    return await model.filter(**kwargs)


async def create_user(
    username: str,
    email: str,
    password: str,
    is_superuser: bool = False,
    is_active: bool = True
) -> User:
    hash_pass = get_password_hash(password)
    return await create_instance(
        User,
        username=username,
        email=email,
        hash_password=hash_pass.decode(),
        is_superuser=is_superuser,
        is_active=is_active,
    )


async def get_parent_pattern(parrent_id: int) -> Pattern:
    return await Pattern.all(
    ).select_related(
        'category'
    ).select_related(
        'section'
    ).prefetch_related(
        Prefetch(
            'variations',
            queryset=PatternVariation.filter(parent_pattern_id=parrent_id),
            to_attr='vars'
        )
    ).filter(
        id=parrent_id
    ).first()


async def add_colors_to_variation(
    variation: PatternVariation,
    colors: list[ColorCreationSchema]
) -> list[Color]:
    colors_by_slug = await Color.get_colors_by_slug()

    pattern_colors = []
    colors_list = []

    for color_data in colors:
        color = colors_by_slug.get(color_data.slug, None)
        if not color:
            print(f'Цвета {color_data.slug} нет в базе данных')
            continue
        pattern_colors.append(PatternColor(pattern=variation, color=color))
        colors_list.append(color)

    await PatternColor.bulk_create(pattern_colors)
    return colors_list


async def add_images_to_variation(
    variation: PatternVariation,
    images: list[ImageCreationSchema],
    base_url: str
) -> list[Image]:
    pattern_images = []
    images_list = []

    for image_data in images:
        img = await create_instance(
            Image,
            image_url=save_image_from_base64(
                image_data.base_64,
                base_url
            ),
            is_main=image_data.is_main
        )
        pattern_images.append(PatternImage(pattern=variation, image=img))
        images_list.append(img)

    await PatternImage.bulk_create(pattern_images)
    return images_list


async def create_variation(
    parent_pattern_id: int,
    colors: list[ColorCreationSchema],
    images: list[ImageCreationSchema],
    base_url: str,
    number_of_variation: str
) -> PatternVariationSchema:
    variation = await create_instance(
        PatternVariation,
        parent_pattern_id=parent_pattern_id,
        number_of_variation=number_of_variation
    )
    colors_list = await add_colors_to_variation(variation, colors)
    images_list = await add_images_to_variation(variation, images, base_url)

    return PatternVariationSchema(
        id=variation.id,
        number_of_variation=number_of_variation,
        colors=colors_list,
        images=images_list,
    )


async def get_pattern_variation(id: int) -> PatternVariation:
    variation = await PatternVariation.all(
    ).select_related(
        'parent_pattern'
    ).select_related(
        'parent_pattern__section'
    ).get_or_none(id=id)

    if not variation:
        raise Error404

    return variation
