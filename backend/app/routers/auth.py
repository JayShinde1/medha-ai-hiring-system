from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from typing import Annotated
from datetime import timedelta

from app.database.database import db_dependency
from app.database.models import Users

from app.schemas.auth_schema import CreateUserRequest, Token

from app.services.auth_service import authenticate_user, create_user

from app.core.security import create_access_token
from app.core.oauth2 import get_current_user


router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)

@router.post("/create-user", status_code = status.HTTP_201_CREATED)
async def register_user(db: db_dependency, create_user_request: CreateUserRequest):
    return create_user(db, create_user_request)


@router.post("/login", response_model = Token) 
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid username or password.")
    token = create_access_token(user.email, user.id, timedelta(minutes = 20))
    return{"access_token": token, "token_type": "bearer"}


@router.get("/get-details")
async def get_user_details(user: Annotated[dict, Depends(get_current_user)], db: db_dependency):
    verify = db.query(Users).filter(Users.id == user['id']).first()
    if not verify:
        raise HTTPException(status_code = 404, details = "User not found")  
    return verify 

