from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.logger import logger
from fastapi.responses import JSONResponse

from ..exception import (
    NotFoundException,
    UnauthorizedException,
    UnsupportedActionException,
)


class ExceptionHandler:
    @staticmethod
    def register_exception_handlers(app: FastAPI):

        @app.exception_handler(Exception)
        async def generic_exception_handler(request: Request, exc: Exception):
            logger.exception(
                f"Unhandled exception on {request.method} {request.url.path}"
            )
            return JSONResponse(
                status_code=500, content={"detail": "Internal server error"}
            )

        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(
            request: Request, exc: RequestValidationError
        ):
            errors = exc.errors()
            lines = []
            for error in errors:
                parts = [str(p) for p in error["loc"] if p != "body"]
                field = parts[-1] if parts else "body"
                message = error["msg"]
                if error["type"].startswith("value_error") and message.startswith(
                    "Value error, "
                ):
                    message = message[len("Value error, ") :]
                if error["type"] == "missing":
                    message = f"{field} is required"
                else:
                    message = f"{field}: {message}"
                lines.append(message)

            return JSONResponse(status_code=400, content={"detail": lines})

        @app.exception_handler(NotFoundException)
        async def not_found_exception_handler(request: Request, exc: NotFoundException):
            return JSONResponse(status_code=404, content={"detail": str(exc)})

        @app.exception_handler(UnauthorizedException)
        async def unauthorized_exception_handler(
            request: Request, exc: UnauthorizedException
        ):
            return JSONResponse(status_code=401, content={"detail": str(exc)})

        @app.exception_handler(UnsupportedActionException)
        async def unsupported_action_exception_handler(
            request: Request, exc: UnsupportedActionException
        ):
            return JSONResponse(status_code=409, content={"detail": str(exc)})
