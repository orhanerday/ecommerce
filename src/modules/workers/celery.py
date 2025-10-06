import logging
from celery import Celery
from src.modules.interface.order import OrdersInterface
from src.entities.order import OrderStatus
from src.modules.interface.products import ProductsInterface
from src.modules.interface.customer import CustomerInterface

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
)


@celery_app.task(name="orders.process_order", acks_late=True)
def process_order(order_id: str, product_id: str, customer_id: str):
    """
    Process order once. If any step fails: mark FAILED and stop.
    No retries, no re-raises.
    """
    from src.database.core import SessionLocal

    db = SessionLocal()

    def fail(reason: str):
        try:
            OrdersInterface.set_order_status(db, order_id, OrderStatus.FAILED)
            db.commit()
        except Exception as e2:
            db.rollback()
            logging.error(f"Order {order_id} secondary fail update error: {e2}")
        logging.warning(f"Order {order_id} FAILED: {reason}")
        return {"order_id": order_id, "status": "FAILED", "reason": reason}

    try:
        # 1) Get dynamic price
        price = ProductsInterface.get_dynamic_price(db, product_id)
        if price is None:
            return fail("price_not_resolved")

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
            return fail("create_order_failed")


        # 3) Decrease customer balance
        if not CustomerInterface.decrease_customer_balance(db, customer_id, price):
            return fail("decrease_customer_balance_failed")

        # 4) Decrease stock
        if not ProductsInterface.decrease_stock(db, product_id):
            return fail("decrease_stock_failed")

        # 5) Mark COMPLETED
        if not OrdersInterface.set_order_status(db, order_id, OrderStatus.COMPLETED):
            return fail("set_status_completed_failed")

        db.commit()
        logging.info(f"Order {order_id} COMPLETED")
        return {"order_id": order_id, "status": "COMPLETED", "price_paid": price}

    except Exception as e:
        db.rollback()
        return fail(f"exception:{e}")
    finally:
        db.close()
