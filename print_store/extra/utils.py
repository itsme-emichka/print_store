import random
import string
import base64
from datetime import timedelta, datetime
from hashlib import sha256

from jose import jwt
import bcrypt

from config import SECRET_KEY, ALGORITHM, MEDIA_ROOT, MEDIA_URL


def get_password_hash(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def save_image_from_base64(base64_data: str, base_url: str) -> str:
    if not base64_data:
        return None
    format, imgstr = base64_data.split(';base64,')
    ext = format.split('/')[-1]
    img_name = sha256(imgstr.encode()).hexdigest()
    image_url = f'{base_url}{MEDIA_URL}{img_name}.{ext}'
    with open(MEDIA_ROOT / f'{img_name}.{ext}', 'wb') as file:
        file.write(base64.b64decode(imgstr))
    return image_url


def generate_random_string(length: int) -> str:
    return ''.join(random.choices(string.ascii_letters, k=length))
