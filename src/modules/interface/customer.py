"""
This module serves as the interface layer for the products domain.

- Define only public-facing API routes or helper functions for cross‑module communication here.
- Keep all business logic in service.py or dedicated builder classes within the build/ folder.
- This separation improves maintainability and enforces clear boundaries between modules.
- In the future, this module can evolve into an API gateway for communication between microservices.
"""

from src.database.core import DbSession
from src.modules.customers import service

class CustomerInterface:
    @staticmethod
    def decrease_customer_balance(db: DbSession, customer_id: str, amount: float) -> bool:
        success = service.decrease_customer_balance(db, customer_id, amount)
        return success