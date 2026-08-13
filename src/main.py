from contextlib import asynccontextmanager

from alembic.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from alembic import command

from .config import settings
from .handler import ExceptionHandler
from .routers import budget_routers, transactions_routers, dashboard_routers


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield


app = FastAPI(title="Personal Budget API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ExceptionHandler.register_exception_handlers(app)

app.include_router(transactions_routers.router)
app.include_router(budget_routers.router)
app.include_router(dashboard_routers.router)

@app.get("/")
def root():
    return {"message": "Budget API is running"}
