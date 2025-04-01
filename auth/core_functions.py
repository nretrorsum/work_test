from datetime import datetime, timedelta
from config import SECRET, ALGORITHM
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, status 
from fastapi.params import Cookie
from db.auth_repository import auth_repository
from typing import Optional, Annotated
from db.model import User
import logging 
logging.basicConfig()

async def create_jwt_token(login: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': login, 'id': user_id, 'role': role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET, algorithm=ALGORITHM)

async def get_current_user(token: Optional[str] = Cookie(alias='access_token', default='')):
    # Отримуємо токен з cookies
    logging.info(f'Token from cookie:{token}')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:
        # Декодуємо токен
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        logging.info(f'JWT payload:{payload}')
        #user_id: str = payload.get("id")
        username: str = payload.get("sub")
        expire: int = payload.get("exp")
        
        if  username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token credentials",
            )
        
        # Перевіряємо чи не закінчився термін дії токена
        if datetime.fromtimestamp(expire) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
            )
        
        # Отримуємо користувача з бази даних
        user = await auth_repository.get_user(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        return user
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
        )
        
user_dependency = Annotated[User, Depends(get_current_user)]