"""
This module serves as the interface layer for the products domain.

- Define only public-facing API routes or helper functions for cross‑module communication here.
- Keep all business logic in service.py or dedicated builder classes within the build/ folder.
- This separation improves maintainability and enforces clear boundaries between modules.
- In the future, this module can evolve into an API gateway for communication between microservices.
"""

from src.database.core import DbSession
from src.modules.products import service
from src.modules.products.build.product import ProductBuilder
from typing import Optional


class ProductsInterface:
    @staticmethod
    def get_dynamic_price(db: DbSession, product_id: str) -> Optional[float]:
        product = service.get_product(db, product_id, cache=False)
        if not product:
            return None
        return ProductBuilder(product).add_dynamic_price().get().current_price

    @staticmethod
    def decrease_stock(db: DbSession, product_id: str) -> bool:
        """Decrease product stock by 1 (or per business rule). Returns True on success, False otherwise."""
        return service.decrease_stock(db, product_id)
