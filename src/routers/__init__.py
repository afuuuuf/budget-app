from .auth_routers import router as auth_router
from .budget_routers import router as budget_router
from .dashboard_routers import router as dashboard_router
from .savings_routers import router as savings_router
from .transactions_routers import router as transaction_router

__all__ = [
    "transaction_router",
    "budget_router",
    "dashboard_router",
    "auth_router",
    "savings_router",
]
