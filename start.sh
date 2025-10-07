#!/bin/bash

# Start Celery worker in the background
celery -A src.modules.workers.celery.celery_app worker --loglevel=info &

# Start FastAPI app using Gunicorn with UvicornWorker
exec gunicorn src.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers 9