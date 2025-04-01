from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from uuid import UUID
from typing import List, Optional
from routers.models.models import TransactionResponse, TransactionUpdate, TransactionRequest
from db.repository import repository
import uuid


transaction_router = APIRouter(prefix="/transactions")

@transaction_router.post("/", response_model=TransactionResponse)
async def create_transaction(transaction_data: TransactionRequest):
    try:
        # Конвертуємо Pydantic модель у dict
        transaction_dict = transaction_data.dict()
        
        # Додаємо автоматичні поля, якщо потрібно
        transaction_dict['id'] = uuid.uuid4()
        transaction_dict['created_at'] = datetime.utcnow()
        transaction_dict['updated_at'] = datetime.utcnow()
        
        # Створюємо транзакцію з продуктами
        created_transaction = await repository.create_transaction_with_items(transaction_dict)
        return created_transaction
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create transaction: {str(e)}"
        )

@transaction_router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    try:
        transactions = await repository.get_transactions_with_items(
            skip=skip,
            limit=limit,
            start_date=start_date,
            end_date=end_date
        )
        return transactions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get transactions: {str(e)}"
        )

@transaction_router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: UUID):
    try:
        transaction = await repository.get_transaction_with_items(transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        return transaction
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get transaction: {str(e)}"
        )

@transaction_router.patch("/{transaction_id}", response_model=TransactionResponse)
async def patch_transaction(
    transaction_id: UUID,
    transaction_update: TransactionUpdate
):
    try:
        # Фільтруємо None значення
        update_data = {
            "cashier_id": transaction_update.cashier_id,
            "total_price": transaction_update.total_price,
            "status": transaction_update.status
        }
        update_data = {k: v for k, v in update_data.items() if v is not None and v != 0}
        
        if not update_data:
            raise ValueError("No fields to update provided")
        
        updated_transaction = await repository.update_transaction(
            transaction_id=transaction_id,
            update_data=update_data
        )
        
        if not updated_transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
            
        return updated_transaction
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update transaction: {str(e)}"
        )

@transaction_router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: UUID):
    try:
        success = await repository.delete_transaction(transaction_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        return {"message": "Transaction deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete transaction: {str(e)}"
        )