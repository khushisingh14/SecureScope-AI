import logging
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


logger = logging.getLogger("securescope")


def _payload(message: str, error_id: str | None = None) -> dict:
    payload = {"detail": message}
    if error_id:
        payload["error_id"] = error_id
    return payload


def configure_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(status_code=exc.status_code, content=_payload(str(exc.detail)), headers=exc.headers)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.info("Request validation failed on %s: %s", request.url.path, exc.errors())
        return JSONResponse(status_code=422, content=_payload("Request validation failed"))

    @app.exception_handler(SQLAlchemyError)
    async def database_exception_handler(request: Request, exc: SQLAlchemyError):
        error_id = str(uuid4())
        logger.exception("Database error %s on %s", error_id, request.url.path)
        return JSONResponse(status_code=500, content=_payload("Database operation failed", error_id))

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        error_id = str(uuid4())
        logger.exception("Unhandled error %s on %s", error_id, request.url.path)
        return JSONResponse(status_code=500, content=_payload("Unexpected server error", error_id))
