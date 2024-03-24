
from typing import Annotated

from controllers.v1.userController import login_for_access_token

from config.config import environ
from models.auth import Token
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from api.v1 import router as v1_router

app = FastAPI()

app.openapi_schema = {}

@app.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    return await login_for_access_token(form_data)

app.include_router(v1_router)

@app.get("/",response_class=RedirectResponse)
async def root():
    #return {"message": "Hello World"}
    return RedirectResponse("docs",status_code=301)