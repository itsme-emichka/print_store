import random
import string
import base64
from hashlib import sha256

from config import (
    MEDIA_ROOT,
    MEDIA_URL,
)
from schemas.order import CartItem


def save_image_from_base64(base64_data: str, base_url: str) -> str:
    if not base64_data:
        return None
    format, imgstr = base64_data.split(';base64,')
    ext = format.split('/')[-1]
    img_name = sha256(imgstr.encode()).hexdigest()
    image_url = f'{base_url}{MEDIA_URL}{img_name}.{ext}'
    with open(MEDIA_ROOT / f'{img_name}.{ext}', 'wb') as file:
        try:
            file.write(base64.b64decode(imgstr))
        except Exception as ex:
            print(ex)
            return None
    return image_url


def generate_random_string(length: int) -> str:
    return ''.join(random.choices(string.ascii_letters, k=length))


def get_final_article_of_pattern_var(
    article: str,
    number: str,
    marker: str
) -> str:
    return f'{article}-{number}-{marker}'


def update_total_price(items: dict[int, CartItem]) -> int:
    cart_total_price = 0
    for item in items.values():
        cart_total_price += float(item.get('price'))
    return cart_total_price


def make_html_list_of_items(items: dict[int, CartItem]) -> str:
    final_html = ''
    for item in items.values():
        item_html = f'''<b>Артикул: {item.get('final_article')}</b><br>
        <ul>
        <li>Количество: {item.get('amount')}</li>
        <li>Цена: {item.get('price')}</li>
        </ul>'''
        final_html += f'{item_html}<br>'

    return final_html
