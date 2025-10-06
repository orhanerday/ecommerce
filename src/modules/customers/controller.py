from fastapi import APIRouter, HTTPException
from uuid import UUID

from src.database.core import DbSession
from .model import CustomerCreate, CustomerResponse
from . import service

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(db: DbSession, customer: CustomerCreate):
    return service.create_customer(db, customer)
