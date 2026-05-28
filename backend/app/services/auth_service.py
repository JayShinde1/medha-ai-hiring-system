from app.core.hashing import (hash_password, verify_password)
from fastapi import HTTPException
from starlette import status
from app.database.models import Users
from app.schemas.auth_schema import CreateUserRequest

def authenticate_user(email, password, db):
    user = db.query(Users).filter(Users.email == email).first()

    if not user: return False
    if not verify_password(password, user.hashed_password):
        return False
    return user 


def create_user(db, create_user_request: CreateUserRequest):

    exciting_user = db.query(Users).filter(Users.email == create_user_request.email).first()
    if exciting_user: 
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User alraady exists.")

    user = Users(
        full_name = create_user_request.full_name,
        email = create_user_request.email,
        hashed_password = hash_password(create_user_request.password),
        role = create_user_request.role,
        is_active = True
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return {'message: ': "User created successfully."}

