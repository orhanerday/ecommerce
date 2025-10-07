from sqlalchemy import Column, Float, String, DateTime, Enum as SAEnum
from sqlalchemy.orm import declarative_base
import uuid
from datetime import datetime, timezone
from enum import Enum as PyEnum

Base = declarative_base()


class OrderStatus(PyEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    customer_id = Column(String(36), nullable=False)
    product_id = Column(String(36), nullable=False)
    price_paid = Column(Float, nullable=True)  # New field for price paid
    status = Column(
        SAEnum(OrderStatus, name="order_status"), default=OrderStatus.PENDING
    )
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
