import re
from uuid import UUID

import bcrypt

from tortoise.models import Model
from tortoise.validators import RegexValidator
from tortoise import fields
from fastadmin import TortoiseModelAdmin, register

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
    hash_password = fields.CharField(max_length=256,)
    token = fields.CharField(max_length=512, null=True,)
    is_superuser = fields.BooleanField(default=False,)
    is_active = fields.BooleanField(default=False)

    def __str__(self):
        return self.username

    @property
    def is_auth(self):
        return bool(self.token)


@register(User)
class UserAdmin(TortoiseModelAdmin):
    list_display = ("id", "username", "is_superuser", "is_active")
    list_display_links = ("id", "username")
    list_filter = ("id", "username", "is_superuser", "is_active")
    search_fields = ("username",)

    async def authenticate(
            self, username: str, password: str) -> UUID | int | None:
        user = await User.filter(username=username, is_superuser=True).first()
        if not user:
            return None
        if not bcrypt.checkpw(password.encode(), user.hash_password.encode()):
            return None
        return user.id
