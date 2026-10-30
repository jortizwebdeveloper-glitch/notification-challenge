from fastapi import FastAPI

import src.core.db.models  # noqa: F401
from src.modules.auth import auth
from src.modules.notification import notification
from src.shared.errors import app_register_errors

app = FastAPI()

app_register_errors(app)

app.include_router(auth)
app.include_router(notification)
