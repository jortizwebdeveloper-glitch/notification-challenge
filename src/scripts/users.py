import random
from src.core.db.models import UserModel, AuthModel, NotificationModel
from src.shared.auth import create_hash

from src.core.db import engine

from sqlalchemy.orm import Session
from sqlalchemy import delete

USERS_MOKCS = [
    {"email": "jortiz@mail.com", "password": "123456"},
    {"email": "imunoz@mail.com", "password": "654231"},
    {"email": "jiom@mail.com", "password": "456789"},
]

NOTIFICATION_MOCKS: list[dict] = [
    {
        "title": "Bienvenido a la plataforma",
        "content": "Gracias por registrarte. Completa tu perfil para empezar.",
        "channel": "email",
    },
    {
        "title": "Verifica tu correo",
        "content": "Haz clic en el enlace que te enviamos para verificar tu cuenta.",
        "channel": "email",
    },
    {
        "title": "Nuevo inicio de sesión",
        "content": "Detectamos un inicio de sesión desde un dispositivo nuevo en Bogotá.",
        "channel": "push",
    },
    {
        "title": "Código de verificación",
        "content": "Tu código es 482913. Expira en 10 minutos.",
        "channel": "sms",
    },
    {
        "title": "Pago recibido",
        "content": "Recibimos tu pago por $59.900. Gracias por tu compra.",
        "channel": "email",
    },
    {
        "title": "Tu pedido fue enviado",
        "content": "El pedido #10234 está en camino. Llegará en 2 a 3 días hábiles.",
        "channel": "push",
    },
    {
        "title": "Recordatorio de cita",
        "content": "Tienes una cita mañana a las 9:00 a. m.",
        "channel": "sms",
    },
    {
        "title": "Contraseña actualizada",
        "content": "Tu contraseña se cambió correctamente. Si no fuiste tú, contáctanos.",
        "channel": "email",
    },
    {
        "title": "Nuevo mensaje",
        "content": "Ana te envió un mensaje: '¿Revisaste el documento?'",
        "channel": "in_app",
    },
    {
        "title": "Suscripción por vencer",
        "content": "Tu plan Pro vence en 5 días. Renuévalo para no perder acceso.",
        "channel": "email",
    },
    {
        "title": "Pedido entregado",
        "content": "El pedido #10234 fue entregado. ¡Esperamos que lo disfrutes!",
        "channel": "push",
    },
    {
        "title": "Oferta especial",
        "content": "20% de descuento en todos los planes anuales hasta el domingo.",
        "channel": "email",
    },
    {
        "title": "Te mencionaron en un comentario",
        "content": "Carlos te mencionó en la tarea 'Diseño del login'.",
        "channel": "in_app",
    },
    {
        "title": "Intento de acceso fallido",
        "content": "Hubo 3 intentos fallidos de inicio de sesión en tu cuenta.",
        "channel": "sms",
    },
    {
        "title": "Factura disponible",
        "content": "Tu factura de octubre ya está disponible para descargar.",
        "channel": "email",
    },
    {
        "title": "Tarea asignada",
        "content": "Se te asignó la tarea 'Integrar pasarela de pagos'.",
        "channel": "in_app",
    },
    {
        "title": "Mantenimiento programado",
        "content": "El servicio estará en mantenimiento el sábado de 2:00 a 4:00 a. m.",
        "channel": "push",
    },
    {
        "title": "Pago rechazado",
        "content": "No pudimos procesar tu pago. Actualiza tu método de pago.",
        "channel": "email",
    },
    {
        "title": "Nuevo seguidor",
        "content": "Laura comenzó a seguirte.",
        "channel": "in_app",
    },
    {
        "title": "Encuesta de satisfacción",
        "content": "Cuéntanos cómo fue tu experiencia. Solo toma 2 minutos.",
        "channel": "email",
    },
]

with Session(engine) as session:
    session.execute(delete(NotificationModel))
    session.execute(delete(AuthModel))
    session.execute(delete(UserModel))

    USERS_ID = []

    for item in USERS_MOKCS:
        user = UserModel(email=item["email"])
        session.add(user)
        session.flush()

        USERS_ID.append(user.id)

        auth = AuthModel(password=create_hash(item["password"]), user_id=user.id)
        session.add(auth)
        session.flush()

    for item in NOTIFICATION_MOCKS:
        notification = NotificationModel(
            title=item["title"],
            content=item["content"],
            channel=item["channel"],
            user_id=random.choice(USERS_ID),
        )
        session.add(notification)

    session.commit()
