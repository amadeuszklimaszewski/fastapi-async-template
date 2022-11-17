from fastapi import FastAPI
from fastapi.routing import APIRouter

from src.routers.user import user_router

app = FastAPI()

router = APIRouter()

router.include_router(user_router)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello world"}
