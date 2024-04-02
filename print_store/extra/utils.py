from datetime import timedelta, datetime
import hashlib

from jose import jwt

from config import SECRET_KEY, ALGORITHM


def get_password_hash(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf8'),
        salt,
        100000,
        512,
    )


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
