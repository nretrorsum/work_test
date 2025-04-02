from pydantic import BaseModel, validator
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class AddNewProduct(BaseModel):
    name: str
    price: int
    quantity: int
    
class ProductResponse(BaseModel):
    id: UUID
    name: str
    price: int
    quantity: int
    created_at: datetime
    
class ProductUpdate(BaseModel):
    name: str
    price: int
    quantity: int

class TransactionItemRequest(BaseModel):
    product_id: UUID
    quantity: int

class TransactionRequest(BaseModel):
    cashier_id: UUID
    total_price: int
    status: str = "paid" 
    items: List[TransactionItemRequest] 
    
    @validator('status')
    def validate_status(cls, v):
        valid_status = ['paid', 'canceled']
        if v not in valid_status:
            raise ValueError(f"Invalid transaction status. Must be one of: {', '.join(valid_status)}")
        return v

class TransactionItemResponse(BaseModel):
    product_id: UUID
    name: str 
    price: int  
    quantity: int  

class TransactionResponse(BaseModel):
    id: UUID
    cashier_id: UUID
    total_price: int
    status: str
    created_at: datetime
    updated_at: datetime
    items: List[TransactionItemResponse]  

class TransactionUpdate(BaseModel):
    cashier_id: Optional[UUID] = None
    total_price: Optional[int] = None
    status: Optional[str] = 'paid'