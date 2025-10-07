from datetime import datetime
from pydantic import BaseModel, ConfigDict
from src.entities.order import OrderStatus


class OrderCreate(BaseModel):
    customer_id: str
    product_id: str


class OrderQueueCreate(BaseModel):
    order_id: str
    customer_id: str
    product_id: str
    status: OrderStatus
    price_paid: float
    created_at: datetime
    updated_at: datetime


class QueuedOrderResponse(OrderCreate):
    order_id: str
    status: OrderStatus


class OrderStatusResponse(BaseModel):
    order_id: str
    product_id: str
    customer_id: str
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
