import random
import string
import base64
from hashlib import sha256

from config import MEDIA_ROOT, MEDIA_URL


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


def get_final_article_of_pattern_var(
    article: str,
    number: str,
    marker: str
) -> str:
    return f'{article}-{number}-{marker}'
