from unittest.mock import MagicMock

import pytest

from main import app
from src.modules.auth import AuthService, get_auth_service


@pytest.fixture
def auth_service():
    mock = MagicMock(spec=AuthService)
    app.dependency_overrides[get_auth_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


async def test_auth_signup_status_200(client, auth_service):
    msg = "Registro relaizado exitosamente"
    auth_service.signup_user.return_value = {"msg": msg}

    data = {"email": "test@test.com", "password": "Password@123"}
    response = await client.post("/signup", data=data)
    assert response.status_code == 200
    assert response.json()["msg"] == msg


async def test_auth_signup_status_422_without_fields(client):
    data = {}
    response = await client.post("/signup", data=data)
    assert response.status_code == 422

    json = response.json()
    assert "detail" in json
    assert json["detail"] == "ValidationError"

    assert "errors" in json

    errors = json["errors"]

    assert len(errors) == 2

    fields = ["email", "password"]

    for err in errors:
        assert err["field"] in fields

        assert "type" in err
        assert err["type"] == "missing"

        assert "msg" in err
        assert type(err["msg"]) == str
        assert len(err["msg"]) > 0


async def test_auth_signup_status_422_invalid_email_format(client):
    data = {"email": "test", "password": "Password@132"}
    response = await client.post("/signup", data=data)
    assert response.status_code == 422

    json = response.json()
    assert "detail" in json
    assert json["detail"] == "ValidationError"

    assert "errors" in json

    errors = json["errors"]

    assert len(errors) == 1

    fields = ["email"]

    for err in errors:
        assert err["field"] in fields

        assert "type" in err
        assert err["type"] == "invalid_email_format"

        assert "msg" in err
        assert type(err["msg"]) == str
        assert len(err["msg"]) > 0


async def test_auth_signup_status_422_invalid_password_format(client):
    data = {"email": "test@test.com", "password": "pass"}
    response = await client.post("/signup", data=data)
    assert response.status_code == 422

    json = response.json()
    assert "detail" in json
    assert json["detail"] == "ValidationError"

    assert "errors" in json

    errors = json["errors"]

    assert len(errors) == 1

    fields = ["password"]

    for err in errors:
        assert err["field"] in fields

        assert "type" in err
        assert err["type"] == "invalid_password_format"

        assert "msg" in err
        assert type(err["msg"]) == str
        assert len(err["msg"]) > 0


async def test_auth_signin_status_200(client, auth_service):
    token = "token"

    auth_service.signin_user.return_value = {"token": token}

    data = {"username": "test@test.com", "password": "Password@123"}
    response = await client.post("/signin", data=data)
    assert response.status_code == 200
    assert "token" in response.json()


async def test_auth_signin_status_422_without_fields(client):
    data = {}
    response = await client.post("/signin", data=data)
    assert response.status_code == 422

    json = response.json()
    assert "detail" in json
    assert json["detail"] == "ValidationError"

    assert "errors" in json

    errors = json["errors"]

    assert len(errors) == 2

    fields = ["username", "password"]

    for err in errors:
        assert err["field"] in fields

        assert "type" in err
        assert err["type"] == "missing"

        assert "msg" in err
        assert type(err["msg"]) == str
        assert len(err["msg"]) > 0


async def test_auth_signin_status_422_invalid_email_format(client):
    data = {"username": "test", "password": "Password@132"}
    response = await client.post("/signin", data=data)
    assert response.status_code == 422

    json = response.json()
    assert "detail" in json
    assert json["detail"] == "ValidationError"

    assert "errors" in json

    errors = json["errors"]

    assert len(errors) == 1

    fields = ["username"]

    for err in errors:
        assert err["field"] in fields

        assert "type" in err
        assert err["type"] == "invalid_email_format"

        assert "msg" in err
        assert type(err["msg"]) == str
        assert len(err["msg"]) > 0
