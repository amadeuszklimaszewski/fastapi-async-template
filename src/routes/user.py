from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter

from src.data_access import UserAsyncDataAccess
from src.dependencies.user import get_user_data_access
from src.models import Token
from src.schemas import RegisterSchema, UserOutputSchema
from src.services.auth import create_access_token
from src.services.exceptions import AlreadyExists
from src.services.user import register_user

user_router = APIRouter(prefix="/users")


@user_router.post(
    "/register/",
    tags=["users"],
    status_code=status.HTTP_201_CREATED,
    response_model=Token,
)
async def register_new_user(
    register_schema: RegisterSchema,
    data_access: UserAsyncDataAccess = Depends(get_user_data_access),
):
    try:
        user = await register_user(data_access, register_schema)
    except AlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with given email already exists",
        )
    else:
        token_data = {"id": user.id}
        access_token = create_access_token(token_data)

        return {"access_token": access_token, "token_type": "bearer"}


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
