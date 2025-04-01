from fastapi import FastAPI
from routers.product_router import product_router
from auth.auth_router import auth_router
from routers.transations_router import transaction_router

app = FastAPI()

app.include_router(
    auth_router,
    tags=['Auth endpoints']
)

app.include_router(
    product_router,
    tags=['Products endpoints']
)

app.include_router(
    transaction_router,
    tags=['Transactions endpoints']
)

