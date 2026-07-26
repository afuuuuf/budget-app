from fastapi import FastAPI
from .routers import transactions_routers
from .config.log_config import setup_logging

setup_logging()
# Schema is now managed by Alembic migrations (see alembic/versions/).
# Run `alembic upgrade head` instead of relying on create_all().

app = FastAPI(title="Personal Budget API")

app.include_router(transactions_routers.router)

@app.get("/")
def root():
    return {"message": "Budget API is running"}