import logging
import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session
from celery.result import AsyncResult

from src.entities.order import OrderStatus
from .model import OrderCreate, OrderStatusResponse
from . import repository

# Configure logging
logger = logging.getLogger(__name__)


def queue_order(db: Session, order: OrderCreate) -> OrderStatusResponse:
    """
    Lightweight order creation following Project A pattern:
    - Generate order_id (UUID)
    - Immediately enqueue Celery task
    - Return PENDING response without DB interaction
    - Worker handles all validation and persistence
    """
    # Import at function level to avoid circular imports (Project A pattern)
    from src.modules.workers.celery import process_order, celery_app
    
    try:
        order_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)

        # Fire async task immediately (Project A pattern)
        task = process_order.delay(
            order_id, 
            str(order.product_id), 
            str(order.customer_id)
        )
        
        # Log task ID for tracking
        logger.info(f"Order {order_id} queued with task ID {task.id}")

        # Return immediately without DB interaction
        return OrderStatusResponse(
            order_id=order_id,
            product_id=order.product_id,
            customer_id=order.customer_id,
            status=OrderStatus.PENDING,
            created_at=now,
            updated_at=now,
        )
        
    except Exception as e:
        logger.error(f"Failed to queue order: {e}")
        raise HTTPException(status_code=500, detail="Failed to queue order")


def get_order(db: Session, order_id: str) -> Optional[OrderStatusResponse]:
    """
    Retrieve order status with optimized DB access.
    Single query, minimal processing.
    """
    try:
        order = repository.get_order(db, order_id)
        if order is None:
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
        logger.error(f"Failed to retrieve order {order_id}: {e}")
        raise


def get_queue_status(order_id: str) -> dict:
    """
    Get Celery task status for an order (Project A pattern).
    Useful for tracking async processing status.
    """
    from src.modules.workers.celery import celery_app
    
    # This would need the task_id stored somewhere
    # For now, returning a simple status check
    return {
        "order_id": order_id,
        "queue_status": "check_db_for_status"
    }


def cancel_order(db: Session, order_id: str) -> bool:
    """
    Cancel order with optimized transaction handling.
    Single transaction for all operations.
    """
    try:
        # Fetch all required entities first
        order = repository.get_order(db, order_id)
        if order is None:
            logger.warning(f"Order {order_id} not found")
            return False

        # Check cancellation eligibility
        if order.status == OrderStatus.CANCELLED:
            logger.info(f"Order {order_id} already cancelled")
            return False

        if order.status != OrderStatus.COMPLETED:
            logger.info(f"Order {order_id} not completed, cannot cancel")
            return False

        # Fetch related entities
        customer = repository.get_customer(db, order.customer_id)
        if customer is None:
            logger.warning(f"Customer {order.customer_id} not found")
            return False
            
        product = repository.get_product(db, order.product_id)
        if product is None:
            logger.warning(f"Product {order.product_id} not found")
            return False

        # Perform all updates in single transaction
        order.status = OrderStatus.CANCELLED
        customer.wallet_balance += order.price_paid
        product.stock += 1
        
        # Single commit
        db.commit()
        
        logger.info(f"Order {order_id} cancelled successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to cancel order {order_id}: {e}")
        db.rollback()
        return False


def set_order_status(db: Session, order_id: str, status: OrderStatus) -> bool:
    """
    Update order status efficiently.
    Note: Commit should be handled by caller for transaction consistency.
    """
    try:
        order = repository.get_order(db, order_id)
        if order is None:
            logger.warning(f"Order {order_id} not found")
            return False

        order.status = status
        # Don't commit here - let caller handle transaction
        logger.info(f"Order {order_id} status set to {status}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to update order {order_id} status: {e}")
        return False


def create_order(db: Session, order_data: dict) -> Optional[object]:
    """
    Create order with minimal overhead.
    Note: Commit should be handled by caller for transaction consistency.
    """
    try:
        order = repository.create_order(db, order_data)
        # Don't commit here - let caller handle transaction
        return order
        
    except Exception as e:
        logger.error(f"Failed to create order: {e}")
        return None