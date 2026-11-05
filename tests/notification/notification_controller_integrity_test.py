import pytest

from src.shared.jwt import create_token_jwt
from tests.helpers import addNotification, addUser, getUser

EMAIL = "test@mail.com"
ENDPOINT = "/notifications"
HEADERS = lambda token: {"Authorization": f"Bearer {token}"}
NOTIFICATION_MOCKS: list[dict] = [
    {
        "title": "Verifica tu correo",
        "content": "# Verifica tu correo electrónico\n\nPara activar tu cuenta necesitamos confirmar que esta dirección es tuya.\n\n## Cómo hacerlo\n\n1. Haz clic en el enlace de abajo.\n2. Inicia sesión si te lo solicitamos.\n3. Verás un mensaje de confirmación.\n\n[Verificar mi cuenta](https://ejemplo.com/verificar)\n\n## Importante\n\n- El enlace **vence en 24 horas**.\n- Si no creaste esta cuenta, puedes ignorar este mensaje.\n- Nunca compartas este enlace con otras personas.\n\n> ¿El enlace no funciona? Copia y pega esta dirección en tu navegador: https://ejemplo.com/verificar\n\nGracias,\n\n**El equipo de seguridad**",
        "channel": "email",
    },
    {
        "title": "Nuevo inicio de sesión",
        "content": "Detectamos un inicio de sesión desde un dispositivo nuevo en Bogotá.",
        "channel": "push",
    },
    {
        "title": "Código de verificación",
        "content": "Tu código de verificación es 482913. Expira en 10 minutos. Si no solicitaste este código, ignora este mensaje y no lo compartas con nadie.",
        "channel": "sms",
    },
]


@pytest.fixture
def jwt_token(session):
    user = getUser(session, EMAIL)
    if not user:
        user = addUser(session, email=EMAIL)
        for item in NOTIFICATION_MOCKS:
            item["user_id"] = user.id
            addNotification(session, item)
        session.expunge_all()

    token = create_token_jwt(str(user.id))

    yield token


async def test_create_notifications_email_status_200(client, jwt_token):
    json = {
        "title": "Bienvenido a la plataforma",
        "content": "# ¡Bienvenido a la plataforma!\n\nGracias por registrarte. Estamos felices de tenerte con nosotros.\n\n## Primeros pasos\n\n1. **Completa tu perfil:** agrega tu nombre, foto y preferencias.\n2. **Verifica tu correo:** así protegemos tu cuenta.\n3. **Explora el panel:** conoce las herramientas principales.\n\n## Lo que puedes hacer\n\n| Función | Descripción |\n|---|---|\n| Panel | Resumen de tu actividad |\n| Proyectos | Crea y organiza tu trabajo |\n| Ajustes | Controla tu privacidad y notificaciones |\n\n> **Consejo:** un perfil completo te ayuda a aprovechar mejor la plataforma.\n\n[Completar mi perfil](https://ejemplo.com/perfil)\n\nSi tienes dudas, escríbenos a soporte@ejemplo.com.\n\nUn saludo,\n\n**El equipo**",
        "channel": "email",
    }
    res = await client.post(
        ENDPOINT,
        headers=HEADERS(jwt_token),
        json=json,
    )

    assert res.status_code == 200
    data = res.json()
    assert "id" in data
    assert json["channel"] == "email"
    assert json["title"] == data["title"]
    assert json["content"] == data["content"]
    assert json["channel"] == data["channel"]


async def test_get_all_notifications_status_200(client, jwt_token):
    res = await client.get(
        ENDPOINT,
        headers=HEADERS(jwt_token),
    )

    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0


ID = 1
NOTI_BY_ID = f"{ENDPOINT}/{ID}"


async def test_get_notifications_by_id_status_200(client, jwt_token):

    res = await client.get(
        NOTI_BY_ID,
        headers=HEADERS(jwt_token),
    )

    assert res.status_code == 200
    data = res.json()
    assert "id" in data
    assert NOTIFICATION_MOCKS[0]["title"] == data["title"]
    assert NOTIFICATION_MOCKS[0]["content"] == data["content"]
    assert NOTIFICATION_MOCKS[0]["channel"] == data["channel"]


async def test_update_notification(client, jwt_token):
    json = {
        "title": "Pago recibido",
        "content": "# Pago recibido\n\nRecibimos tu pago correctamente. Gracias por tu compra.\n\n## Detalle de la transacción\n\n| Concepto | Valor |\n|---|---|\n| Pedido | #10234 |\n| Monto pagado | $59.900 |\n| Método de pago | Tarjeta de crédito |\n| Estado | Aprobado |\n\n## Qué sigue\n\n- Prepararemos tu pedido en las próximas horas.\n- Te avisaremos cuando salga de bodega.\n- Podrás descargar tu factura desde tu cuenta.\n\n[Ver mi pedido](https://ejemplo.com/pedidos/10234)\n\nGuarda este correo como comprobante.\n\n**El equipo de ventas**",
        "channel": "email",
    }

    res = await client.put(NOTI_BY_ID, headers=HEADERS(jwt_token), json=json)

    assert res.status_code == 200
    data = res.json()

    assert ID == data["id"]
    assert json["title"] == data["title"]
    assert json["content"] == data["content"]
    assert json["channel"] == data["channel"]


async def test_delete_notification(client, jwt_token):
    res = await client.delete(NOTI_BY_ID, headers=HEADERS(jwt_token))

    assert res.status_code == 200
    data = res.json()

    assert data == 1
