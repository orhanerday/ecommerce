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
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_reject_on_worker_lost=True,
)


@celery_app.task(
    bind=True,
    name="orders.process_order",
    acks_late=True,
    autoretry_for=(SQLAlchemyError,),
    retry_backoff=True,
    retry_backoff_max=60,
    retry_kwargs={"max_retries": 3},
)
def process_order(self, order_id: str, product_id: str, customer_id: str) -> Dict:
    """
    Process order with proper locking to ensure exactly one succeeds when stock=1.
    All orders (success or failure) are saved to the database.
    """
    from src.database.core import SessionLocal
    from src.modules.interface.order import OrdersInterface
    from src.entities.order import OrderStatus, Order
    from src.entities.product import Product
    from src.entities.customer import Customer
    from src.modules.interface.products import ProductsInterface
    
    db = SessionLocal()
    
    try:
        # Check if order already exists (idempotency)
        existing_order = db.query(Order).filter_by(order_id=order_id).first()
        if existing_order:
            if existing_order.status == OrderStatus.COMPLETED:
                logger.info(f"Order {order_id} already completed")
                return {
                    "order_id": order_id,
                    "status": "COMPLETED",
                    "price_paid": float(existing_order.price_paid)
                }
            elif existing_order.status == OrderStatus.FAILED:
                logger.info(f"Order {order_id} already failed")
                return {
                    "order_id": order_id,
                    "status": "FAILED",
                    "reason": "Previously failed"
                }
        
        # CRITICAL: Lock product row FIRST to prevent race conditions
        product = db.query(Product).filter(
            Product.id == product_id
        ).with_for_update().first()  # Pessimistic lock - only one worker can hold this
        
        if not product:
            # Create failed order for product not found
            if not existing_order:
                order = Order(
                    order_id=order_id,
                    customer_id=customer_id,
                    product_id=product_id,
                    price_paid=0,
                    status=OrderStatus.FAILED
                )
                db.add(order)
                db.commit()
            raise ValueError(f"Product {product_id} not found")
        
        # Calculate price first (needed for order record)
        price = ProductsInterface.get_dynamic_price(db, product_id)
        if price is None or price <= 0:
            # Create failed order for invalid price
            if not existing_order:
                order = Order(
                    order_id=order_id,
                    customer_id=customer_id,
                    product_id=product_id,
                    price_paid=0,
                    status=OrderStatus.FAILED
                )
                db.add(order)
                db.commit()
            raise ValueError(f"Invalid price for product {product_id}")
        
        # Get customer with lock
        customer = db.query(Customer).filter(
            Customer.customer_id == customer_id
        ).with_for_update().first()
        
        if not customer:
            # Create failed order for customer not found
            if not existing_order:
                order = Order(
                    order_id=order_id,
                    customer_id=customer_id,
                    product_id=product_id,
                    price_paid=price,
                    status=OrderStatus.FAILED
                )
                db.add(order)
                db.commit()
            raise ValueError(f"Customer {customer_id} not found")
        
        # Create or update order to PENDING first
        if not existing_order:
            order = Order(
                order_id=order_id,
                customer_id=customer_id,
                product_id=product_id,
                price_paid=price,
                status=OrderStatus.PENDING
            )
            db.add(order)
            db.flush()  # Make order visible in this transaction but don't commit yet
        else:
            existing_order.status = OrderStatus.PENDING
            existing_order.price_paid = price
            order = existing_order
        
        # NOW check stock AFTER creating the order and acquiring lock
        if product.stock <= 0:
            # Mark order as FAILED due to insufficient stock
            order.status = OrderStatus.FAILED
            db.commit()
            logger.warning(f"Order {order_id} FAILED: Insufficient stock")
            raise ValueError(f"Insufficient stock for product {product_id}")
        
        # Check customer balance
        if customer.wallet_balance < price:
            # Mark order as FAILED due to insufficient balance
            order.status = OrderStatus.FAILED
            db.commit()
            logger.warning(f"Order {order_id} FAILED: Insufficient balance")
            raise ValueError(f"Insufficient balance for customer {customer_id}")
        
        # All validations passed - execute the transaction
        
        # Decrease stock atomically
        product.stock -= 1
        
        # Decrease customer balance atomically
        customer.wallet_balance -= price
        
        # Mark order as completed
        order.status = OrderStatus.COMPLETED
        
        # SINGLE COMMIT for all changes
        db.commit()
        
        logger.info(f"Order {order_id} COMPLETED successfully")
        
        return {
            "order_id": order_id,
            "status": "COMPLETED",
            "price_paid": float(price)
        }
        
    except ValueError as e:
        # Business logic failures - order should already be saved as FAILED
        error_msg = str(e)
        logger.warning(f"Order {order_id} processing failed: {error_msg}")
        
        return {
            "order_id": order_id,
            "status": "FAILED",
            "reason": error_msg
        }
        
    except SQLAlchemyError as e:
        # Database errors - retry
        db.rollback()
        logger.error(f"Database error processing order {order_id}: {e}, will retry")
        raise
        
    except Exception as e:
        # Unexpected errors - try to save as failed
        db.rollback()
        logger.error(f"Unexpected error processing order {order_id}: {e}")
        
        try:
            db2 = SessionLocal()
            try:
                existing = db2.query(Order).filter_by(order_id=order_id).first()
                if not existing:
                    order = Order(
                        order_id=order_id,
                        customer_id=customer_id,
                        product_id=product_id,
                        price_paid=0,
                        status=OrderStatus.FAILED
                    )
                    db2.add(order)
                else:
                    existing.status = OrderStatus.FAILED
                db2.commit()
            finally:
                db2.close()
        except Exception:
            pass
        
        return {
            "order_id": order_id,
            "status": "FAILED",
            "reason": f"Unexpected error: {str(e)}"
        }
        
    finally:
        db.close()