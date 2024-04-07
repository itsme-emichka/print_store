import re

from tortoise import fields
from tortoise.models import Model
from tortoise.validators import RegexValidator
from tortoise.fields.base import OnDelete


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


class PatternVariation(BaseModel):
    colors = fields.ManyToManyField(
        'models.Color',
        through='PatternColor',
        description='Образец паттерна в определенном цвете',
        related_name='pattern',
        on_delete=OnDelete.CASCADE,
    )
    images = fields.ManyToManyField(
        'models.Image',
        through='PatternImage',
        description='Картинки паттерна в определенном цвете',
        related_name='pattern',
        null=True,
        on_delete=OnDelete.SET_NULL,
    )
    parent_pattern = fields.ForeignKeyField(
        'models.Pattern',
        description='Родительский паттерн',
        related_name='variations',
        on_delete=OnDelete.CASCADE,
    )


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
