from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from models.user import User, UserInDB
from models.auth import Token

from dependencies.auth import authenticate_user, create_access_token, get_current_active_user

from config.config import environ
from dependencies.dbConnector import get_db_connector


try:
    db = get_db_connector()
except AttributeError as e:
    print(e)
    exit()

async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    return current_user

async def create_user(
    user: UserInDB
) -> UserInDB:
    return True

def get_user(username: str) -> UserInDB:
    query_response = db.query("SELECT username, email, full_name, disabled from users where username = ?",[(username)])

    if query_response:
        user = query_response[0]
        return UserInDB(
            username = user[0],
            email = user[1],
            full_name = user[2],
            disabled = user[3]
            )