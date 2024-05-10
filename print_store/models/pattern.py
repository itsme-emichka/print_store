import re

from tortoise import fields
from tortoise.models import Model
from tortoise.validators import RegexValidator
from tortoise.fields.base import OnDelete
from fastadmin import TortoiseModelAdmin, register

from config import SLUG_PATTERN


class BaseModel(Model):
    id = fields.BigIntField(pk=True)

    class Meta:
        abstract = True


class StoreSection(BaseModel):
    name = fields.CharField(
        description='Название раздела',
        max_length=512,
        unique=True,
    )
    slug = fields.CharField(
        description='Слаг раздела',
        max_length=256,
        unique=True,
        validators=[RegexValidator(SLUG_PATTERN, re.A)],
    )
    article_marker = fields.CharField(
        description='Маркер раздела',
        max_length=8,
        unique=True,
    )

    sections_by_slug = dict()

    @classmethod
    async def get_sections_by_slug(cls) -> dict:
        if not cls.sections_by_slug:
            await cls.update_sections_by_slug()
        return cls.sections_by_slug

    @classmethod
    async def update_sections_by_slug(cls):
        for section in await cls.all():
            cls.sections_by_slug[str(section.slug)] = section
        return cls.sections_by_slug

    @classmethod
    async def create(cls, using_db=None, **kwargs):
        instance = await super().create(using_db, **kwargs)
        await cls.update_sections_by_slug()
        return instance


class Category(BaseModel):
    name = fields.CharField(
        description='Название категории принта',
        max_length=512,
        unique=True,
    )
    slug = fields.CharField(
        description='Слаг категории принта',
        max_length=256,
        unique=True,
        validators=[RegexValidator(SLUG_PATTERN, re.A)],
    )

    categories_by_slug = dict()

    @classmethod
    async def get_categories_by_slug(cls) -> dict:
        if not cls.categories_by_slug:
            await cls.update_categories_by_slug()
        return cls.categories_by_slug

    @classmethod
    async def update_categories_by_slug(cls):
        for category in await cls.all():
            cls.categories_by_slug[str(category.slug)] = category
        return cls.categories_by_slug

    @classmethod
    async def create(cls, using_db=None, **kwargs):
        instance = await super().create(using_db, **kwargs)
        await cls.update_categories_by_slug()
        return instance


class Material(BaseModel):
    name = fields.CharField(
        description='Название материала',
        max_length=512,
        unique=True
    )
    slug = fields.CharField(
        description='Слаг материала',
        max_length=256,
        unique=True,
        validators=[RegexValidator(SLUG_PATTERN, re.A)],
    )
    width = fields.IntField(
        description='Ширина материала в мм',
    )
    density = fields.IntField(
        description='Плотность материала в г/м^3',
    )


class Pattern(BaseModel):
    name = fields.CharField(
        description='Название принта',
        max_length=512,
        unique=True,
        null=True,
    )
    article = fields.CharField(
        description='Артикул принта',
        max_length=64,
    )
    slug = fields.CharField(
        description='Слаг принта',
        max_length=256,
        unique=True,
        validators=[RegexValidator(SLUG_PATTERN, re.A)],
        null=True,
    )
    category = fields.ForeignKeyField(
        'models.Category',
        description='Категория принта',
        related_name='category',
        null=True,
        on_delete=OnDelete.SET_NULL,
    )
    price = fields.DecimalField(
        description='Цена принта',
        max_digits=16,
        decimal_places=2,
    )
    cover = fields.CharField(
        description='Обложка принта',
        max_length=2048,
        null=True,
    )
    description = fields.TextField(null=True)
    horizontal_rapport = fields.DecimalField(
        description='Горизонтальный раппорт в см',
        max_digits=3,
        decimal_places=1
    )
    vertical_rapport = fields.DecimalField(
        description='Вертикальный раппорт в см',
        max_digits=3,
        decimal_places=1
    )
    section = fields.ForeignKeyField(
        'models.StoreSection',
        related_name='pattern',
    )
    variations: fields.ReverseRelation['PatternVariation']


class PatternVariation(BaseModel):
    parent_pattern = fields.ForeignKeyField(
        'models.Pattern',
        description='Родительский паттерн',
        related_name='variations',
        to_field='id',
        on_delete=OnDelete.CASCADE,
    )
    number_of_variation = fields.CharField(
        description='Номер цветовой вариации',
        max_length=8,
    )

    @property
    async def colors(self):
        return await Color.filter(pattern_color__pattern=self)

    @property
    async def images(self):
        return await Image.filter(pattern_image__pattern=self)


class Color(BaseModel):
    name = fields.CharField(
            description='Название цвета',
            max_length=512,
            unique=True,
    )
    slug = fields.CharField(
        description='Слаг цвета',
        max_length=256,
        unique=True,
        validators=[RegexValidator(SLUG_PATTERN, re.A)],
    )
    hex = fields.CharField(max_length=7)

    colors_by_slug = dict()

    @classmethod
    async def get_colors_by_slug(cls) -> dict:
        if not cls.colors_by_slug:
            await cls.update_color_by_slug()
        return cls.colors_by_slug

    @classmethod
    async def update_color_by_slug(cls):
        for color in await cls.all():
            cls.colors_by_slug[str(color.slug)] = color
        return cls.colors_by_slug

    @classmethod
    async def create(cls, using_db=None, **kwargs):
        instance = await super().create(using_db, **kwargs)
        await cls.update_color_by_slug()
        return instance


class PatternColor(BaseModel):
    pattern = fields.ForeignKeyField(
        'models.PatternVariation',
        related_name='pattern_color',
    )
    color = fields.ForeignKeyField(
        'models.Color',
        related_name='pattern_color',
    )


class Image(BaseModel):
    name = fields.CharField(
            description='Название цвета',
            max_length=512,
            unique=True,
            null=True,
    )
    image_url = fields.CharField(
        max_length=1024,
    )
    is_main = fields.BooleanField(default=False,)


class PatternImage(BaseModel):
    pattern = fields.ForeignKeyField(
        'models.PatternVariation',
        related_name='pattern_image',
    )
    image = fields.ForeignKeyField(
        'models.Image',
        related_name='pattern_image',
    )


@register(Color)
class ColorAdmin(TortoiseModelAdmin):
    list_display = ('name', 'slug', 'hex',)


@register(Category)
class CategoryAdmin(TortoiseModelAdmin):
    list_display = ('name', 'slug',)


class UserShoppingCart(BaseModel):
    user = fields.ForeignKeyField(
        'models.User',
        related_name='shopping_cart',
    )
    pattern_variation = fields.ForeignKeyField(
        'models.PatternVariation',
        related_name='shopping_cart',
    )
    material = fields.ForeignKeyField(
        'models.Material',
        related_name='shopping_cart',
    )
    amount = fields.IntField(
        description='Количество товара в корзине',
    )
