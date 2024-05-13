from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware

from routers import characteristics, pattern, order
from database.db import TORTOISE_ORM
from config import ALLOWED_ORIGINS, SECRET_KEY

from extra.utils import generate_random_string


load_dotenv(override=True)


app = FastAPI()

app.include_router(pattern.router)
app.include_router(characteristics.router)
app.include_router(order.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.middleware('http')
async def session_middleware(request: Request, call_next):
    sesid = request.session.get('id')
    cart = request.session.get('cart')
    if not sesid:
        sesid = generate_random_string(64)
        request.session['id'] = sesid
    if not cart:
        request.session['cart'] = {'items': dict(),
                                   'total_price': 0}
    response: Response = await call_next(request)

    return response


app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
