from fastapi import APIRouter, HTTPException
from uuid import UUID

from src.database.core import DbSession
from .model import ProductResponse
from . import service

router = APIRouter(prefix="/products", tags=["products"])


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    response_model_exclude={"initial_stock"},
    status_code=200,
)
def get_product(db: DbSession, product_id: str):
    product = service.get_product(db, product_id, cache=True)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
