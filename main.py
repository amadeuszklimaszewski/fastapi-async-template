from fastapi import FastAPI
from fastapi.routing import APIRouter

from src.routes.auth import auth_router
from src.routes.user import user_router

app = FastAPI()

router = APIRouter()

router.include_router(user_router)
router.include_router(auth_router)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello world"}


# HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
