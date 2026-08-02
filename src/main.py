from fastapi import FastAPI
from .routers import transactions_routers, budget_routers
from contextlib import asynccontextmanager
from alembic.config import Config
from alembic import command

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield

app = FastAPI(title="Personal Budget API")

app.include_router(transactions_routers.router)
app.include_router(budget_routers.router)

@app.get("/")
def root():
    return {"message": "Budget API is running"}