from src.modules.auth import AuthModel
from src.modules.users import UserModel


def addUser(session, email):
    user = UserModel(email=email)
    session.add(user)
    session.flush()
    return user


def addAuth(session, password, user_id):
    auth = AuthModel(password=password, user_id=user_id)
    session.add(auth)
    session.flush()
    return auth
