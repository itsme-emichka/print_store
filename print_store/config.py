import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(override=True)

SECRET_KEY: str = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_DAYS = 7
ALGORITHM = "HS256"
TOKEN_TYPE: str = 'Bearer'

BASE_DIR: Path = Path(__file__).resolve().parent
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
SLUG_PATTERN: str = r'^[-|_a-z0-9]*$'
EMAIL_PATTERN: str = r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+'
BASE64_PATTERN: str = r'^data:image/(png|jpeg|jpg);base64,.+$'
