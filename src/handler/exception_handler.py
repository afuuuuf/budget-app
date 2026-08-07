from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ..exception import NotFoundException

class ExceptionHandler:

    @staticmethod
    def register_exception_handlers(app: FastAPI):
        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            errors = exc.errors()
            first_error = errors[0]
            field = first_error["loc"][-1]

            if first_error["type"] == "missing":
                message = f"{field} is required"
            else:
                message = first_error["msg"]

            return JSONResponse(status_code=400, content={"detail": message})

        @app.exception_handler(NotFoundException)
        async def not_found_exception_handler(request: Request, exc: NotFoundException):
            return JSONResponse(status_code=404, content={"detail": str(exc)})