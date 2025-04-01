from db.auth_abstract_repository import AbstractAuthRepository
from db.model import User
from sqlalchemy import insert, select, delete
import uuid
from datetime import datetime
from fastapi import HTTPException
from typing import Optional
from enum import Enum
from db.db_connection import async_session
import logging
logging.basicConfig()

class AuthRepository(AbstractAuthRepository):
    def __init__(self, db):
        self.db = db
        
    async def register_user(self, user_dict: dict):
            async with self.db.begin() as session:
                try:
                    user = User(
                        username=user_dict['username'],
                        password_hash=user_dict['password'],
                        role=user_dict['role']
                    )
                    session.add(user)
                    return {'status': '201', 'detail': 'user created'}
                except Exception as e:
                    await session.rollback()
                    raise HTTPException(status_code=500, detail=f"Error: {e}")
    
    async def get_user(self, login: str) -> Optional[dict]:
        async with self.db.begin() as session:
            try:
                # Більш сучасний стиль запиту
                stmt = select(User).where(User.username == login)
                user = await session.scalar(stmt)  # Простий спосіб отримати один результат
                
                if not user:
                    return None
                    
                return {
                    'id': str(user.id),
                    'username': user.username,
                    'password_hash': user.password_hash,
                    'role': user.role.value if isinstance(user.role, Enum) else user.role,
                    'created_at': user.created_at.isoformat() if user.created_at else None
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error: {e}")
    
    async def delete_user(self, login: str):
        pass
    
auth_repository = AuthRepository(async_session)