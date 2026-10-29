import src.core.db.models

from fastapi import FastAPI
from src.modules.auth import auth
from src.modules.notification import notification

from src.shared.errors import app_register_errors

app = FastAPI()

app_register_errors(app)

app.include_router(auth)
app.include_router(notification)
