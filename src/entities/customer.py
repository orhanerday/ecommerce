from sqlalchemy import Column, String, DateTime, Float, CheckConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, nullable=False, unique=True)
    wallet_balance = Column(Float, default=5000.0)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    __table_args__ = (
        CheckConstraint("wallet_balance >= 0", name="check_wallet_balance_non_negative"),
    )
