from fastapi import FastAPI
#from src.modules.orders.controller import router as todos_router
from src.modules.customers.controller import router as customer_router
from src.modules.products.controller import router as product_router
from src.modules.orders.controller import router as order_router

def register_routes(app: FastAPI):
    app.include_router(customer_router, prefix="/api/v1")
    app.include_router(product_router, prefix="/api/v1")
    app.include_router(order_router, prefix="/api/v1")