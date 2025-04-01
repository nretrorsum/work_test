from pydantic import BaseModel, validator
from enum import Enum

class UserRole(Enum):
    admin = 'admin'
    cachier = 'cashier'
    
    @validator('role_name')
    def validate_role(cls, v):
        valid_roles = ['cashier', 'admin']
        if v not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        return v

class RegisterUser(BaseModel):
    username: str
    password: str
    role: UserRole
    
class LoginUser(BaseModel):
    username: str
    password: str
