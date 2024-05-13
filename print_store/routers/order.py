from datetime import datetime
from typing import Any

from fastapi import APIRouter, Request, HTTPException, status
from schemas.order import OrderForm
from extra.utils import make_html_list_of_items, send_message

from config import CORPORATE_MAIL


router = APIRouter(prefix='/order')


@router.get('')
async def get_cart(request: Request) -> dict[str, Any]:
    return request.session['cart']


@router.post('')
async def make_order(user_data: OrderForm, request: Request):
    if not request.session['cart']['items']:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Корзина пуста')
    html = f'''<h1>Заказ</h1>
    <b>{datetime.now()}</b>
    <h3>Данные заказчика:</h3>
    <ul>
    <li>Имя: {user_data.name}</li>
    <li>Телефон: {user_data.phone_number}</li>
    <li>Почта: {user_data.email}</li>
    </ul>
    <h3>Адрес доставки:</h3>
    {user_data.adress}
    <h3>Товары:</h3>
    {make_html_list_of_items(request.session['cart']['items'])}
    <h3>Сумма:</h3>
    {request.session['cart']['total_price']}
    '''

    send_message(CORPORATE_MAIL, 'Заказ', html)

    return 'Заказ оформлен'
