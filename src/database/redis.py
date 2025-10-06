from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import os

""" You can add a DATABASE_URL environment variable to your .env file """
#DATABASE_URL = os.getenv("DATABASE_URL")
# TODO: remove the hardcoded fallback for production use
#DATABASE_URL = "mysql+pymysql://root:supersecret@127.0.0.1:3306/ecommerce?charset=utf8mb4"

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(
    DATABASE_URL,
    pool_size=50,
    max_overflow=100,
    pool_timeout=30,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
DbSession = Annotated[Session, Depends(get_db)]

