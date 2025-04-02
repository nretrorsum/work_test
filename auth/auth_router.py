from fastapi import APIRouter, HTTPException, Response
from auth.models.models import RegisterUser, LoginUser
from db.auth_repository import auth_repository
from passlib.context import CryptContext
from datetime import timedelta
from auth.core_functions import user_dependency
from auth.core_functions import create_jwt_token
import logging
logging.basicConfig()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

auth_router = APIRouter(
    prefix = '/api/auth',
)

@auth_router.post('/register')
async def register_user(user: RegisterUser):
    user_dict = {
        'username': user.username,
        'password': bcrypt_context.hash(user.password),
        'role': user.role.value  
    }
    return await auth_repository.register_user(user_dict)

@auth_router.post('/login')
async def login_user(user: LoginUser, response: Response):
    checked_user = await auth_repository.get_user(login=user.username)
    if not checked_user:
        raise HTTPException(status_code=401, detail='Not authenticated')
    
    if not bcrypt_context.verify(user.password, checked_user['password_hash']):
        raise HTTPException(status_code=401, detail='Not authenticated')

    token = await create_jwt_token(
        login=user.username,
        user_id=str(checked_user['id']),
        role= str(checked_user['role']),
        expires_delta=timedelta(minutes=15)
    )
    
    response.set_cookie(
        key='access_token',  
        value=token,  
        max_age=900,
        path='/',
        secure=False,  
        httponly=True, 
        samesite='lax'
    )
    
    return {'status': '200', 'detail': 'Authenticated'}

@auth_router.post("/logout")
async def logout_user(response: Response):
    try:
        response.set_cookie(
            key="access_token",
            value="",
            max_age=0,
            path="/",
            secure=False,
            httponly=True,
            samesite="lax"
        )
        
        return {"status": "200", "detail": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Logout error: {str(e)}"
        )

@auth_router.get("/me")
async def get_user_profile(user: user_dependency):
    return {"user_id": user['id'], "username": user['username'], "role": user['role']}