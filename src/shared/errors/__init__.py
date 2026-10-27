import logging

from fastapi import status, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .exceptions import (
    AppError,
    ForbiddenError,
    InfrastructureError,
    AlreadyExistsError,
)

STATUS_BY_ERROR: dict[type[AppError], int] = {
    ForbiddenError: status.HTTP_403_FORBIDDEN,
    InfrastructureError: status.HTTP_503_SERVICE_UNAVAILABLE,
    AlreadyExistsError: status.HTTP_409_CONFLICT,
}
logger = logging.getLogger(__name__)


def get_status_by_error(exc: AppError) -> int:
    for cls in type(exc).mro():
        if cls in STATUS_BY_ERROR:
            return STATUS_BY_ERROR[cls]

    return status.HTTP_500_INTERNAL_SERVER_ERROR


def app_error_handle(_, exc: AppError) -> JSONResponse:

    status_code = get_status_by_error(exc)

    if status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.error("Error interno: %s", exc.msg, exc_info=exc)
        msg = "Internal Error Server"
    else:
        msg = exc.msg

    return JSONResponse(status_code=status_code, content={"detail": msg})


ERROR_MESSAGE = {"missing": "Campo obligatorio"}


def request_error_handle(_, exc: RequestValidationError):
    errors = []
    exc_errors = exc.errors()
    logger.error("Request Error: %s", exc_errors, exc_info=exc)
    for err in exc_errors:
        type_error = err["type"]
        field = err["loc"][-1] if err["loc"] else "request"
        msg = ERROR_MESSAGE.get(type_error)

        errors.append({"field": field, "type": type_error, "msg": msg or err["msg"]})

    return JSONResponse(
        status_code=422, content={"detail": "RequestValidationError", "errors": errors}
    )


def app_register_errors(app: FastAPI):
    app.add_exception_handler(AppError, app_error_handle)
    app.add_exception_handler(RequestValidationError, request_error_handle)
