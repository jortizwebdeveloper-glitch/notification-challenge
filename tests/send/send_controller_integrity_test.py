import logging

import pytest

from src.shared.jwt import create_token_jwt
from tests.helpers import async_add_notification, async_add_user, async_get_user

EMAIL = "test@mail.com"
ENDPOINT = "/send"
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
async def jwt_token(scope_async_session):
    async with scope_async_session() as session:
        user = await async_get_user(session, EMAIL)
        if not user:
            user = await async_add_user(session, email=EMAIL)
            for item in NOTIFICATION_MOCKS:
                item["user_id"] = user.id
                await async_add_notification(session, item)
            await session.commit()

        token = create_token_jwt(str(user.id))

        yield token


async def test_send_notification_status_200(client, jwt_token, caplog, worker):
    caplog.set_level(logging.INFO)
    noti = await client.get("/notifications", headers=HEADERS(jwt_token))
    assert noti.status_code == 200

    noti_json = noti.json()
    assert len(noti_json) > 0

    ID = noti_json[0]["id"]
    SEND_BY_ID = f"{ENDPOINT}/{ID}"

    res = await client.post(SEND_BY_ID, headers=HEADERS(jwt_token))
    assert res.status_code == 200

    jobs = res.json()
    assert "job_ids" in jobs

    completed = await worker.run_check()
    assert completed == len(jobs["job_ids"])


async def test_get_send_notification_status_200(client, jwt_token):
    res = await client.get(ENDPOINT, headers=HEADERS(jwt_token))

    assert res.status_code == 200
