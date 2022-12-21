from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.data_access import UserAsyncDataAccess
from src.data_access.exceptions import DoesNotExist
from src.dependencies.user import get_user_data_access
from src.models import Token
from src.services.auth import authenticate_user, create_access_token
from src.services.exceptions import InvalidCredentials

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login/", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    data_access: UserAsyncDataAccess = Depends(get_user_data_access),
):
    try:
        user = await authenticate_user(
            data_access, form_data.username, form_data.password
        )
    except (DoesNotExist, InvalidCredentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization failed. Please check your credentials and try again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        token_data = {"id": str(user.id)}
        access_token = create_access_token(token_data)
        return {"access_token": access_token, "token_type": "bearer"}
