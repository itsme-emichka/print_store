import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(override=True)

BASE_DIR: Path = Path(__file__).resolve().parent

SECRET_KEY: str = os.getenv('SECRET_KEY')

ALLOWED_ORIGINS = (
    'http://127.0.0.1:8000',
    'http://127.0.0.1',
    'http://localhost',
    'http://localhost:8000',
    'http://localhost:8080',
)

# TOKEN
ACCESS_TOKEN_EXPIRE_DAYS = 7
ALGORITHM = "HS256"
TOKEN_TYPE: str = 'Bearer'

# MEDIA
MEDIA_URL: str = 'media/'
MEDIA_ROOT: Path = BASE_DIR / MEDIA_URL
PROTOCOL: str = 'http'

# DATABASE
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

# REGEX_PATTERNS
SLUG_PATTERN: str = r'^[-_a-z0-9]*$'
EMAIL_PATTERN: str = r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+'
BASE64_PATTERN: str = r'^data:image/(png|jpeg|jpg);base64,.+$'
HEX_PATTERN: str = r'^#[a-z0-9]{6}$'
