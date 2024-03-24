

from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from controllers.v1.userController import login_for_access_token
from dependencies.auth import get_current_active_user

from models.auth import Token
from models.user import User

router = APIRouter(
    prefix = '/users'
)

@router.get('/all')
async def getUsers(
    user = Depends(get_current_active_user)
) -> list[User]:

    return []

@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    return await login_for_access_token(form_data)


@router.get("/me/", response_model=User)
async def read_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
