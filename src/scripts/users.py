from src.modules.users.infra.user_model import UserModel
from src.core.db import engine

from sqlalchemy.orm import Session
from sqlalchemy import delete

with Session(engine) as session:
    session.execute(delete(UserModel))
    session.add(UserModel(email="jortiz.webdeveloper@gmail.com"))
    session.commit()
