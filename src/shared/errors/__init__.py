import logging

from fastapi import status, FastAPI
from fastapi.responses import JSONResponse

from .exceptions import AppError, ForbiddenError

STATUS_BY_ERROR: dict[type[AppError], int] = {ForbiddenError: status.HTTP_403_FORBIDDEN}
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


def app_register_errors(app: FastAPI):
    app.add_exception_handler(AppError, app_error_handle)
