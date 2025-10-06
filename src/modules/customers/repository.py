import logging
from src.database.core import DbSession
from src.entities.customer import Customer


def add_customer(db: DbSession, customer_create):
    customer = Customer(username=customer_create.username, wallet_balance=5000.0)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    logging.info(f"Created new customer: {customer.customer_id}")
    return customer


def get_customer(db: DbSession, customer_id: str) -> Customer | None:
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()
