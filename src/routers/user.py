from uuid import UUID

from fastapi import Depends, status
from fastapi.routing import APIRouter

from src.models.user import User
from src.schemas.user import RegisterSchema, UserOutputSchema
from src.services.user import UserService

user_router = APIRouter(prefix="/users")


@user_router.post(
    "/register/",
    tags=["users"],
    status_code=status.HTTP_201_CREATED,
    response_model=UserOutputSchema,
)
async def register_user(
    user_register_schema: RegisterSchema,
    user_service: UserService = Depends(),
):
    ...


@user_router.get(
    "/",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    response_model=list[UserOutputSchema],
)
async def get_users() -> list[UserOutputSchema]:
    ...


@user_router.get(
    "/{user_id}/",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    response_model=UserOutputSchema,
)
async def get_user(user_id: UUID) -> UserOutputSchema:
    ...
