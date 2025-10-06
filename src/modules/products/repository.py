from uuid import UUID
from typing import Optional
import logging

from src.database.core import DbSession
from src.entities.product import Product as ProductORM
from src.modules.products.model import ProductResponse


def get_product(db: DbSession, product_id: str):
    product = db.query(ProductORM).filter(ProductORM.id == str(product_id)).first()
    if not product:
        return None
    return product
