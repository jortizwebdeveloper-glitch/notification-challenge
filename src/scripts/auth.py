from src.core.db import engine

from src.modules.users.infra.user_model import UserModel
from src.modules.auth.infra.auth_model import AuthModel

from sqlalchemy.orm import Session
from sqlalchemy import delete
from src.shared.auth import create_hash

list = [
    {"email": "jortiz.webdeveloper@gmail.com", "password": "123456"},
    {"email": "luminei01@gmail.com", "password": "456789"},
    {"email": "jiom147147@gmail.com", "password": "789123"},
]
with Session(engine) as session:
    session.execute(delete(AuthModel))
    session.execute(delete(UserModel))

    for l in list:
        user = UserModel(email=l["email"])
        session.add(user)
        session.flush()

        auth = AuthModel(user_id=user.id, password=create_hash(l["password"]))
        session.add(auth)

    session.commit()
