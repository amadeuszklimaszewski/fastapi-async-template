from uuid import UUID

from fastapi import Depends, status
from fastapi.routing import APIRouter
from fastapi_another_jwt_auth import AuthJWT
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.database.connection import get_db
from src.dependencies.users import authenticate_user
from src.models.user import User
from src.schemas.jwt import TokenSchema
from src.schemas.user import LoginSchema, RegisterSchema, UserOutputSchema
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
    session: AsyncSession = Depends(get_db),
):
    user_schema = await user_service.register_user(
        user_register_schema, session=session
    )
    return user_schema


@user_router.post(
    "/login/",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    response_model=TokenSchema,
)
async def login_user(
    user_login_schema: LoginSchema,
    auth_jwt: AuthJWT = Depends(),
    user_service: UserService = Depends(),
    session: AsyncSession = Depends(get_db),
):
    user = await user_service.authenticate(**user_login_schema.dict(), session=session)
    user_schema = User.from_orm(user)
    access_token = auth_jwt.create_access_token(subject=user_schema.json())

    return TokenSchema(access_token=access_token)


@user_router.get(
    "/",
    tags=["users"],
    dependencies=[Depends(authenticate_user)],
    status_code=status.HTTP_200_OK,
    response_model=list[UserOutputSchema],
)
async def get_users(session: AsyncSession = Depends(get_db)) -> list[UserOutputSchema]:
    result = await session.exec(select(User))
    return [UserOutputSchema.from_orm(user) for user in result.all()]


@user_router.get(
    "/profile/",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    response_model=UserOutputSchema,
)
async def get_logged_user(
    request_user: User = Depends(authenticate_user),
) -> UserOutputSchema:
    return UserOutputSchema.from_orm(request_user)


@user_router.get(
    "/{user_id}/",
    tags=["users"],
    dependencies=[Depends(authenticate_user)],
    status_code=status.HTTP_200_OK,
    response_model=UserOutputSchema,
)
async def get_user(
    user_id: UUID, session: AsyncSession = Depends(get_db)
) -> UserOutputSchema:
    result = await session.exec(select(User).where(User.id == user_id))
    return User.from_orm(result.first())
