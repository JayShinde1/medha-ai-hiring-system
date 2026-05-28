#This is to decode the jwt token and to get the current user
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import HTTPException, Depends
from starlette import status
from jose import JWTError, jwt

from app.core.security import SECRET_KEY, ALGORITHM

oauth2_bearer = OAuth2PasswordBearer(tokenUrl = '/auth/login')

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        email: str = payload.get('email')
        user_id: int = payload.get('id')

        if email is None or user_id is None:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Could not validate user.")
        return {'email': email, 'id': user_id}

    except JWTError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Could not validate user.")