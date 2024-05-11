from tortoise import Tortoise, run_async

from config import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DATABASE
)

TORTOISE_ORM = {
    'connections': {
        'default': f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}'
    },
    'apps': {
        'models': {
            'models': ['models.pattern', 'aerich.models'],
            'default_connection': 'default',
        },
    },
}


async def setup():
    await Tortoise.init(TORTOISE_ORM)
    await Tortoise.generate_schemas()


if __name__ == '__main__':
    run_async(setup())
