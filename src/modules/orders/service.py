import logging
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.entities.order import OrderStatus
from .model import OrderCreate, OrderStatusResponse
from . import repository


def queue_order(db: Session, order: OrderCreate) -> OrderStatusResponse | None:
    """
    New lightweight create:
    - Do NOT touch DB.
    - Generate order_id (UUID).
    - Immediately enqueue Celery task to validate + persist + process.
    - Return PENDING response snapshot.
    """
    from src.modules.workers.celery import process_order  # local import avoids circulars
    try:
        order_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)

        # Fire async processing (worker will:
        #  - validate customer/product
        #  - calculate dynamic price
        #  - create order row if missing
        #  - decrement stock & wallet
        #  - update status)
        process_order.delay(order_id, str(order.product_id), str(order.customer_id))

        return OrderStatusResponse(
            order_id=order_id,
            product_id=order.product_id,
            customer_id=order.customer_id,
            status=OrderStatus.PENDING,
            created_at=now,
            updated_at=now,
        )
    except Exception as e:
        logging.error(f"Failed to queue order. Error: {e}")
        raise

def get_order(db: Session, order_id: str) -> OrderStatusResponse | None:
    """Retrieve the status of an order by its ID.

    Returns an OrderStatusResponse or None if the order does not exist.
    """
    try:
        order = repository.get_order(db, order_id)
        if order is None:
            logging.warning(f"Order with ID {order_id} not found.")
            return None

        return OrderStatusResponse(
            order_id=order.order_id,
            product_id=order.product_id,
            customer_id=order.customer_id,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
    except Exception as e:
        logging.error(f"Failed to retrieve order status. Error: {e}")
        raise
    
def cancel_order(db: Session, order_id: str) -> bool:
    """Cancel an order by its ID.

    Returns True if the cancellation request was successful, False otherwise.
    """
    try:
        order = repository.get_order(db, order_id)
        if order is None:
            logging.warning(f"Order with ID {order_id} not found.")
            return False

        if order.status in [OrderStatus.CANCELLED]:
            logging.info(f"Order with ID {order_id} is already {order.status}. No action taken.")
            return False

        if order.status != OrderStatus.COMPLETED :
            logging.info(f"Order with ID {order_id} is not completed. No action taken.")
            return False

        order.status = OrderStatus.CANCELLED
        customer = repository.get_customer(db, order.customer_id)
        if customer is None:
            logging.warning(f"Customer with ID {order.customer_id} not found.")
            return False
        customer.wallet_balance += order.price_paid
        product = repository.get_product(db, order.product_id)
        if product is None:
            logging.warning(f"Product with ID {order.product_id} not found.")
            return False
        product.stock += 1
        db.commit()
        logging.info(f"Order with ID {order_id} has been cancelled.")
        return True
    except Exception as e:
        logging.error(f"Failed to cancel order with ID {order_id}. Error: {e}")
        db.rollback()
        return False

def set_order_status(db: Session, order_id: str, status: OrderStatus) -> bool:
    """Set the status of an order.

    Returns True if the status update was successful, False otherwise.
    """
    try:
        order = repository.get_order(db, order_id)
        if order is None:
            logging.warning(f"Order with ID {order_id} not found.")
            return False

        order.status = status
        logging.info(f"Order with ID {order_id} status updated to {status}.")
        return True
    except Exception as e:
        logging.error(f"Failed to update status for order ID {order_id}. Error: {e}")
        return 

def create_order(db: Session, order_data: dict):
    try:
        order = repository.create_order(db, order_data)
        return order
    except Exception as e:
        logging.error(f"Failed to create order. Error: {e}")
        return None