from fastapi import FastAPI
from .database.core import engine, Base
from .entities.customer import Customer  # Import models to register them
from .entities.order import Order  # Import models to register them
from .entities.product import Product  # Import models to register them
from .api.v1.api import register_routes
from .core.logging import configure_logging, LogLevels


configure_logging(LogLevels.info)

app = FastAPI()

register_routes(app)
