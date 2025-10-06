from uuid import uuid4, UUID
from .model import CustomerCreate, CustomerResponse
from src.entities.customer import Customer as CustomerORM
from sqlalchemy.orm import Session
from . import repository
import logging


def create_customer(db: Session, customer: CustomerCreate) -> CustomerResponse:
    try:
        customer = repository.add_customer(db, customer)
        return customer
    except Exception as e:
        logging.error(f"Failed to create customer. Error: {str(e)}")
        raise

def decrease_customer_balance(db: Session, customer_id: str, amount: float) -> bool:
    """Decrease the balance of a customer by a specified amount.

    Returns True if successful, False otherwise.
    """
    try:
        customer = repository.get_customer(db, customer_id)
        if customer is None:
            logging.warning(f"Customer with ID {customer_id} not found.")
            return False

        if customer.wallet_balance < amount:
            logging.warning(f"Insufficient balance for customer ID {customer_id}. Current balance: {customer.wallet_balance}, requested decrease: {amount}.")
            return False

        customer.wallet_balance -= amount
        logging.info(f"Decreased balance for customer ID {customer_id} by {amount}. New balance: {customer.wallet_balance}.")
        return True
    except Exception as e:
        logging.error(f"Failed to decrease balance for customer ID {customer_id}. Error: {str(e)}")
        return False