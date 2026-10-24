from fastapi import FastAPI, APIRouter

app = FastAPI()


root = APIRouter(prefix="")

@root.get("/")
def get_root():
    return "Hello world"

app.include_router(root)