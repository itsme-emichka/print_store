import re

from tortoise import fields
from tortoise.models import Model
from tortoise.validators import RegexValidator
from tortoise.fields.base import OnDelete
from fastadmin import TortoiseModelAdmin, register


class BaseModel(Model):
    id = fields.BigIntField(pk=True)

    class Meta:
        abstract = True


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
        validators=[RegexValidator('^[-|_a-z0-9]*$', re.A)],
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


class Pattern(BaseModel):
    name = fields.CharField(
        description='Название принта',
        max_length=512,
        unique=True,
        null=True,
    )
    slug = fields.CharField(
        description='Слаг принта',
        max_length=256,
        unique=True,
        validators=[RegexValidator('^[-|_a-z0-9]*$', re.A)],
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
    variations: fields.ReverseRelation['PatternVariation']


class PatternVariation(BaseModel):
    # colors: fields.ManyToManyRelation['Color'] = fields.ManyToManyField(
    #     'models.Color',
    #     through='PatternColor',
    #     description='Образец паттерна в определенном цвете',
    #     related_name='pattern',
    #     on_delete=OnDelete.CASCADE,
    # )
    # images = fields.ManyToManyField(
    #     'models.Image',
    #     through='PatternImage',
    #     description='Картинки паттерна в определенном цвете',
    #     related_name='pattern',
    #     null=True,
    #     on_delete=OnDelete.SET_NULL,
    # )
    parent_pattern = fields.ForeignKeyField(
        'models.Pattern',
        description='Родительский паттерн',
        related_name='variations',
        to_field='id',
        on_delete=OnDelete.CASCADE,
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
        validators=[RegexValidator('^[-|_a-z0-9]*$', re.A)],
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
