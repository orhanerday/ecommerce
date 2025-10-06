import logging
from fastapi import APIRouter, HTTPException

from src.database.core import DbSession
from .model import OrderCreate, OrderStatusResponse
from . import service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post(
    "/",
    response_model=OrderStatusResponse,
    status_code=202,
)
def queue_order(db: DbSession, order_data: OrderCreate):
    order = service.queue_order(db, order_data)
    if not order:
        raise HTTPException(status_code=400, detail="Failed to create order")
    return order


@router.get(
    "/{order_id}",
    response_model=OrderStatusResponse,
    status_code=200,
)
def get_order(db: DbSession, order_id: str):
    order = service.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post(
    "/{order_id}/cancel",
    status_code=202,
)
def cancel_order(db: DbSession, order_id: str):
    success = service.cancel_order(db, order_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to cancel order")
    return {"message": f"Cancellation request for order {order_id} accepted."}
