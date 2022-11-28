from uuid import UUID

from fastapi import Depends, status
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.data_access import UserAsyncDataAccess
from src.dependencies.database import get_db
from src.schemas import IDOutputSchema, RegisterSchema, UserOutputSchema
from src.services import UserService

user_router = APIRouter(prefix="/users")


@user_router.post(
    "/register/",
    tags=["users"],
    status_code=status.HTTP_201_CREATED,
    response_model=IDOutputSchema,
)
async def register_user(
    register_schema: RegisterSchema,
    db: AsyncSession = Depends(get_db),
):
    data_access = UserAsyncDataAccess(db)
    user_service = UserService(data_access)

    user = await user_service.register_user(register_schema)
    return user


@user_router.get(
    "/",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    response_model=list[UserOutputSchema],
)
async def get_users(
    db: AsyncSession = Depends(get_db),
):
    data_access = UserAsyncDataAccess(db)
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
    db: AsyncSession = Depends(get_db),
):
    data_access = UserAsyncDataAccess(db)
    user = await data_access.get(pk=user_id)
    return UserOutputSchema.from_orm(user)
