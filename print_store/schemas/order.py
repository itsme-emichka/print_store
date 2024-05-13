from typing import Annotated

from pydantic import BaseModel, EmailStr
from fastapi import Query

from config import PHONE_NUMBER


class OrderForm(BaseModel):
    name: str
    phone_number: Annotated[str, Query(pattern=PHONE_NUMBER)]
    email: EmailStr
    adress: str


class CartItem(BaseModel):
    pattern_variation_id: int
    parent_pattern_id: int
    final_article: str
    amount: int
    price: float
