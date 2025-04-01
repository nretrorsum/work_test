from fastapi import APIRouter, HTTPException, status
from routers.models.models import AddNewProduct, ProductResponse, ProductUpdate
from db.repository import repository
from typing import List
from uuid import UUID

product_router = APIRouter(
    prefix='/api/product',
)

@product_router.post('/add_product')
async def add_product(product: AddNewProduct):
    try:
        # Не передаємо id і created_at - вони генеруються в репозиторії
        product_data = {
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity if product.quantity is not None else 0
        }
        
        created_product = await repository.create_product(product_data=product_data)
        return created_product
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
        
@product_router.get("/", response_model=List[ProductResponse])
async def list_products(skip: int = 0, limit: int = 100):
    try:
        products = await repository.get_products(skip=skip, limit=limit)
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch products: {str(e)}"
        )

@product_router.get("/{product_id}")
async def get_product(product_id: UUID):
    try:
        product = await repository.get_product(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch product: {str(e)}"
        )
        
@product_router.put('/update_product/{product_id}', response_model=ProductResponse)
async def update_product(
    product_id: UUID,
    product_update: ProductUpdate,
):
    try:
        # Фільтруємо None значення та встановлюємо дефолтні
        update_data = {
            "name": product_update.name,
            "price": product_update.price,
            "quantity": product_update.quantity if product_update.quantity is not None else 0
        }
        # Видаляємо поля з None значеннями
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        if not update_data:
            raise ValueError("No fields to update provided")
        
        updated_product = await repository.update_product(
            product_id=product_id,
            product_data=update_data
        )
        
        if not updated_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
            
        return updated_product
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update product: {str(e)}"
        )
        
@product_router.patch('/patch_product/{product_id}', response_model=ProductResponse)
async def patch_product(
    product_id: UUID,
    product_update: ProductUpdate,
):
    try:
        # Фільтруємо None значення та встановлюємо дефолтні
        update_data = {
            "name": product_update.name,
            "price": product_update.price,
            "quantity": product_update.quantity if product_update.quantity is not None else None
        }
        # Видаляємо поля з None значеннями
        update_data = {k: v for k, v in update_data.items() if v is not None and v is not 0}
        
        if not update_data:
            raise ValueError("No fields to update provided")
        
        patched_product = await repository.patch_product(
            product_id=product_id,
            update_data=update_data
        )
        
        if not patched_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
            
        return patched_product
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to patch product: {str(e)}"
        )
        
