from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(
        "product_id", String(36), primary_key=True, default=uuid.uuid4, index=True
    )
    name = Column(String, nullable=False)
    description = Column(String)
    base_price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    initial_stock = Column(Integer, nullable=False, default=0)

    @property
    def product_id(self):
        return self.id
