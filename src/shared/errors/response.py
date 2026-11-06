from typing import TypedDict

from pydantic import BaseModel


class ErrorsType(TypedDict):
    field: str
    type: str
    msg: str


class ResponseError(BaseModel):
    detail: str


class ResponseValidationError(BaseModel):
    detail: str
    errors: list[ErrorsType]


ERROR_DESCRIPTIONS = {
    400: "Solicitud inválida",
    401: "No autenticado",
    403: "Sin permisos",
    404: "Recurso no encontrado",
    409: "Conflicto con un recurso existente",
    422: "Error de validación de los datos enviados",
}


def get_error_response(*codes: int) -> dict:

    response = {
        422: {
            "model": ResponseValidationError,
            "description": ERROR_DESCRIPTIONS[422],
        }
    }

    for code in codes:
        response[code] = {
            "model": ResponseError,
            "description": ERROR_DESCRIPTIONS.get(code, "Error"),
        }

    return response
