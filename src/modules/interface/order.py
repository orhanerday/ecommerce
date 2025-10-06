"""
This module serves as the interface layer for the products domain.

- Define only public-facing API routes or helper functions for cross‑module communication here.
- Keep all business logic in service.py or dedicated builder classes within the build/ folder.
- This separation improves maintainability and enforces clear boundaries between modules.
- In the future, this module can evolve into an API gateway for communication between microservices.
"""

from src.database.core import DbSession
from src.entities.order import OrderStatus
from src.modules.orders import service

class OrdersInterface:
    @staticmethod
    def set_order_status(db: DbSession, order_id: str, status: OrderStatus) -> bool:
        success = service.set_order_status(db, order_id, status)
        return success
    
    def create_order(db: DbSession, order_payload: dict):
        order = service.create_order(db, order_payload)
        return order