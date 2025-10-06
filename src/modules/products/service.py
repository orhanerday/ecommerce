import os
from uuid import UUID

from sqlalchemy import BOOLEAN

from src.modules.products.build.product import ProductBuilder
from .model import ProductResponse
from src.entities.product import Product as ProductORM
from sqlalchemy.orm import Session
from . import repository
import logging
import redis
import json
from cachetools import TTLCache

inproc_cache = TTLCache(maxsize=10_000, ttl=30)

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
r = redis.from_url(redis_url, max_connections=1000)

def get_product(db: Session, product_id: str, cache: bool) -> ProductResponse | None:
    """
    Retrieve a product with optional multi‑tier caching (in‑proc + Redis).
    When cache=False: always hit DB and do not read/write caches.
    """
    try:
        if cache:
            # In‑process cache tier
            hit = inproc_cache.get(product_id)
            if hit:
                return hit

            # Redis cache tier
            cache_key = f"product:{product_id}"
            cached_bytes = r.get(cache_key)
            if cached_bytes:
                try:
                    obj = json.loads(cached_bytes.decode("utf-8"))
                    model = ProductResponse(**obj)
                    inproc_cache[product_id] = model
                    return model
                except (UnicodeDecodeError, ValueError) as e:
                    logging.warning(f"Corrupt cache for key {cache_key}: {e}")

        # DB fetch
        product = repository.get_product(db, product_id)
        if product is None:
            logging.warning(f"Product with ID {product_id} not found.")
            return None

        response = ProductResponse(
            product_id=product.id,
            name=product.name,
            description=product.description or "",
            base_price=product.base_price,
            current_price=0,
            stock=product.stock,
            initial_stock=product.initial_stock,
        )
        response = ProductBuilder(response).add_dynamic_price().get()

        if cache:
            cache_key = f"product:{product_id}"
            payload = response.model_dump_json()
            # Fire-and-forget cache set (ignore errors)
            try:
                r.setex(cache_key, 10, payload)
                inproc_cache[product_id] = response
            except Exception as ce:
                logging.debug(f"Cache set failed for {cache_key}: {ce}")

        return response
    except Exception as e:
        logging.error(f"Failed to retrieve product {product_id}. Error: {e}")
        raise

def decrease_stock(db: Session, product_id: UUID, amount: int = 1) -> bool:
    """Decrease stock for a product by a specified amount.

    Returns True if successful, False otherwise.
    """
    try:
        product = repository.get_product(db, str(product_id))
        if product is None:
            logging.warning(f"Product with ID {product_id} not found.")
            return False

        if product.stock < amount:
            logging.warning(f"Insufficient stock for product ID {product_id}. Current stock: {product.stock}, requested decrease: {amount}.")
            return False

        product.stock -= amount
        logging.info(f"Decreased stock for product ID {product_id} by {amount}. New stock: {product.stock}.")
        return True
    except Exception as e:
        logging.error(f"Failed to decrease stock for product ID {product_id}. Error: {str(e)}")
        return False
    
    
def increase_stock(db: Session, product_id: UUID, amount: int = 1) -> bool:
    """Increase stock for a product by a specified amount.

    Returns True if successful, False otherwise.
    """
    try:
        product = repository.get_product(db, str(product_id))
        if product is None:
            logging.warning(f"Product with ID {product_id} not found.")
            return False

        product.stock += amount
        logging.info(f"Increased stock for product ID {product_id} by {amount}. New stock: {product.stock}.")
        return True
    except Exception as e:
        logging.error(f"Failed to increase stock for product ID {product_id}. Error: {str(e)}")
        return False