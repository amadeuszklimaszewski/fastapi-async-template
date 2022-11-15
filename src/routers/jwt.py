from fastapi import APIRouter, Depends, Response, status

from src.dependencies.users import authenticate_user
from src.models.user import User

jwt_router = APIRouter(prefix="/token")


@jwt_router.post("/verify/", status_code=status.HTTP_204_NO_CONTENT)
def verify_token(request_user: User = Depends(authenticate_user)) -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)
