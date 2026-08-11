from fastapi import FastAPI, Request, logger
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ..exception import NotFoundException, UnsupportedActionException

class ExceptionHandler:

    @staticmethod
    def register_exception_handlers(app: FastAPI):

        @app.exception_handler(Exception)
        async def generic_exception_handler(request: Request, exc: Exception):
            logger.exception(f"Unhandled exception on {request.method} {request.url.path}")
            return JSONResponse(status_code=500, content={"detail": "Internal server error"})

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

        @app.exception_handler(UnsupportedActionException)
        async def unsupported_action_exception_handler(request: Request, exc: UnsupportedActionException):
            return JSONResponse(status_code=409, content={"detail": str(exc)})