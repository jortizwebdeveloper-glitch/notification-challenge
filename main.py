from fastapi import FastAPI

import src.core.db.models  # noqa: F401
from src.core.arq import arq_pool
from src.modules.auth.controller.router import auth
from src.modules.notification.controller.router import notification
from src.modules.send.controller.router import send
from src.shared.errors import app_register_errors

app = FastAPI(lifespan=arq_pool)

app_register_errors(app)

app.include_router(auth)
app.include_router(notification)
app.include_router(send)
