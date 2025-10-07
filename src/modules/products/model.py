from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ProductResponse(BaseModel):
    product_id: UUID
    name: str
    description: str
    base_price: float
    current_price: float
    stock: int
    initial_stock: int

    model_config = ConfigDict(from_attributes=True)
