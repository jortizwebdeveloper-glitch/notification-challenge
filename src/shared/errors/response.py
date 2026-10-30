from typing import TypedDict

from pydantic import BaseModel


class ErrorsType(TypedDict):
    field: str
    type: str
    msg: str


class DTORequestValidationError(BaseModel):
    detail: str
    errors: list[ErrorsType]


COMMON_REPONSES = {422: {"model": DTORequestValidationError}}
