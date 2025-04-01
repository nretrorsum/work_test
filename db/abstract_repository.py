from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class AbstractRepository(ABC):
    
    # --- Product Operations ---
    @abstractmethod
    async def get_products(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def get_product(self, product_id: UUID) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def update_product(self, product_id: UUID, product_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def patch_product(self, product_id: UUID, update_data: Dict[str, Any]) -> Dict[str, Any]:

        pass
    
    @abstractmethod
    async def delete_product(self, product_id: UUID) -> bool:
        pass
    
    # --- Transaction Operations ---
    @abstractmethod
    async def create_transaction_with_items(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def get_transactions_with_items(self, skip: int = 0, limit: int = 100, 
                             start_date: Optional[datetime] = None, 
                             end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def get_transaction_with_items(self, transaction_id: UUID) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def update_transaction(self, transaction_id: UUID, 
                               update_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def delete_transaction(self, transaction_id: UUID) -> bool:
        pass