from fastapi import FastAPI, APIRouter
from src.modules.auth import auth


app = FastAPI()


root = APIRouter(prefix="")

@root.get("/")
def get_root():
    return "Hello world"

app.include_router(root)

app.include_router(auth)