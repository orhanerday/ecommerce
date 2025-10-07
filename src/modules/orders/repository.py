import logging
from src.database.core import DbSession
from src.entities.order import Order
from src.entities.customer import Customer
from src.entities.product import Product


def create_order(db: DbSession, order_data: dict) -> Order:
    """Persist a new order.

    order_data should contain: customer_id, product_id, price_paid, status.
    Timestamps & order_id are provided by model defaults.
    """
    order = Order(
        order_id=order_data.get("order_id"),
        customer_id=order_data["customer_id"],
        product_id=order_data["product_id"],
        price_paid=order_data.get("price_paid"),
        status=order_data["status"],
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    logging.info(f"Created new order: {order.order_id}")
    return order


def get_customer(db: DbSession, customer_id: str) -> Customer | None:
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()


def get_product(db: DbSession, product_id: str) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()


def get_order(db: DbSession, order_id: str) -> Order | None:
    return db.query(Order).filter(Order.order_id == order_id).first()
