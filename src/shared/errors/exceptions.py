class AppError(Exception):
    """Raíz de todos los errores de la aplicación"""

    def __init__(self, msg: str = "Error inesperado"):
        self.msg = msg
        super().__init__(msg)


class AuthenticationError(AppError):
    """Autenticacion invalida"""


class ForbiddenError(AppError):
    """Sin permisos para acceder"""


class NotFoundError(AppError):
    """No encontrado"""


class AlreadyExistsError(AppError):
    """Registro ya existente"""


class InfrastructureError(AppError):
    """Errores de infraestructura (db, server, etc)"""
