import logging
from typing import Dict
from celery import Celery
from celery.utils.log import get_task_logger
from sqlalchemy.exc import SQLAlchemyError

logger = get_task_logger(__name__)

celery_app = Celery(
    "ecommerce",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Add performance optimizations from Project A
    task_acks_late=True,
    worker_prefetch_multiplier=1,  # Prevent worker from prefetching too many tasks
    task_reject_on_worker_lost=True,
)


@celery_app.task(
    bind=True,
    name="orders.process_order",
    acks_late=True,
    autoretry_for=(SQLAlchemyError,),  # Auto-retry on DB errors like Project A
    retry_backoff=True,
    retry_backoff_max=60,
    #retry_kwargs={"max_retries": 3},  # Limited retries for critical operations
)
def process_order(self, order_id: str, product_id: str, customer_id: str) -> Dict:
    """
    Process order with optimized database handling.
    Creates session internally like Project A.
    Single transaction with rollback on failure.
    """
    # Import here to avoid circular dependencies (like Project A pattern)
    from src.database.core import SessionLocal
    from src.modules.interface.order import OrdersInterface
    from src.entities.order import OrderStatus
    from src.modules.interface.products import ProductsInterface
    from src.modules.interface.customer import CustomerInterface
    
    # Create session inside task (Project A pattern)
    db = SessionLocal()
    
    try:
        # Start transaction implicitly
        
        # 1) Get dynamic price
        price = ProductsInterface.get_dynamic_price(db, product_id)
        if price is None:
            raise ValueError(f"Price not resolved for product {product_id}")

        # 2) Create order (PENDING) if not exists
        created = OrdersInterface.create_order(
            db,
            {
                "order_id": order_id,
                "customer_id": customer_id,
                "product_id": product_id,
                "price_paid": price,
                "status": OrderStatus.PENDING,
            },
        )
        if not created:
            raise ValueError(f"Failed to create order {order_id}")

        # 3) Decrease customer balance
        if not CustomerInterface.decrease_customer_balance(db, customer_id, price):
            raise ValueError(f"Failed to decrease balance for customer {customer_id}")

        # 4) Decrease stock
        if not ProductsInterface.decrease_stock(db, product_id):
            raise ValueError(f"Failed to decrease stock for product {product_id}")

        # 5) Mark COMPLETED
        if not OrdersInterface.set_order_status(db, order_id, OrderStatus.COMPLETED):
            raise ValueError(f"Failed to set status COMPLETED for order {order_id}")

        # Single commit at the end (like Project A)
        db.commit()
        
        logger.info("Order %s COMPLETED for task %s", order_id, self.request.id)
        
        return {
            "order_id": order_id,
            "status": "COMPLETED",
            "price_paid": float(price)
        }
        
    except ValueError as e:
        # Business logic failures - mark as FAILED, don't retry
        db.rollback()
        try:
            # Create new session for status update
            OrdersInterface.set_order_status(db, order_id, OrderStatus.FAILED)
            db.commit()
        except Exception as e2:
            logger.error(f"Failed to update order {order_id} status to FAILED: {e2}")
        
        logger.warning(f"Order {order_id} FAILED: {str(e)}")
        
        # Don't retry business logic failures
        self.request.callbacks = None
        return {
            "order_id": order_id,
            "status": "FAILED",
            "reason": str(e)
        }
        
    except SQLAlchemyError:
        # Database errors - let Celery retry automatically
        db.rollback()
        logger.error(f"Database error processing order {order_id}, will retry")
        raise
        
    except Exception as e:
        # Unexpected errors - mark as FAILED
        db.rollback()
        logger.error(f"Unexpected error processing order {order_id}: {e}")
        
        try:
            OrdersInterface.set_order_status(db, order_id, OrderStatus.FAILED)
            db.commit()
        except Exception:
            pass
            
        return {
            "order_id": order_id,
            "status": "FAILED",
            "reason": f"Unexpected error: {str(e)}"
        }
        
    finally:
        db.close()