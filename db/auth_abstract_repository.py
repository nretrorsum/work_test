from abc import ABC, abstractmethod

class AbstractAuthRepository(ABC):
    #@abstractmethod
    async def register_user(self, user_dict: dict):
        pass
    
    #@abstractmethod
    async def get_user(self, login: str):
        pass
    
    async def delete_user(self, login: str):
        pass