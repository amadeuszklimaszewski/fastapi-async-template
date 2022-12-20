from uuid import UUID

from fastapi import Depends, status
from fastapi.routing import APIRouter

from src.data_access import UserAsyncDataAccess
from src.dependencies.user import get_user_data_access
from src.schemas import IDOutputSchema, RegisterSchema, UserOutputSchema
from src.services.user import register_user

user_router = APIRouter(prefix="/users")


@user_router.post(
    "/register/",
    tags=["users"],
    status_code=status.HTTP_201_CREATED,
    response_model=IDOutputSchema,
)
async def register_new_user(
    register_schema: RegisterSchema,
    data_access: UserAsyncDataAccess = Depends(get_user_data_access),
):
    user = await register_user(data_access, register_schema)
    return user


@user_router.get(
    "/",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    response_model=list[UserOutputSchema],
)
async def get_users(
    data_access: UserAsyncDataAccess = Depends(get_user_data_access),
):
    users = await data_access.get_many()
    return [UserOutputSchema.from_orm(user) for user in users]


@user_router.get(
    "/{user_id}/",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    response_model=UserOutputSchema,
)
async def get_user(
    user_id: UUID,
    data_access: UserAsyncDataAccess = Depends(get_user_data_access),
):
    user = await data_access.get(pk=user_id)
    return UserOutputSchema.from_orm(user)
