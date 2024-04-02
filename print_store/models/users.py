import re

from tortoise.models import Model
from tortoise.validators import RegexValidator
from tortoise import fields

from config import SLUG_PATTERN, EMAIL_PATTERN


class User(Model):
    id = fields.BigIntField(pk=True,)
    username = fields.CharField(
        max_length=256,
        unique=True,
        validators=[RegexValidator(SLUG_PATTERN, re.A)],
    )
    email = fields.CharField(
        max_length=256,
        unique=True,
        validators=[RegexValidator(EMAIL_PATTERN, re.A)],
    )
    password = fields.BinaryField()
    salt = fields.BinaryField()
    token = fields.CharField(max_length=512, null=True,)

    @property
    def is_auth(self):
        return bool(self.token)
