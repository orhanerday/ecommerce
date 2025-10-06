from uuid import UUID
from pydantic import BaseModel, ConfigDict


class CustomerCreate(BaseModel):
    username: str


class CustomerResponse(BaseModel):
    customer_id: UUID
    username: str
    wallet_balance: float
    model_config = ConfigDict(from_attributes=True)
