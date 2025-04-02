from db.abstract_repository import AbstractRepository
from db.db_connection import async_session
from sqlalchemy import select, insert, update, desc, delete
from db.model import Product, User, Transaction, transaction_product
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
import uuid

class Repository(AbstractRepository):
    def __init__(self,db):
        self.db = db
    
    async def get_products(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        async with self.db.begin() as session:
            query = select(Product).order_by(desc(Product.price)).offset(skip).limit(limit)
            result = await session.execute(query)
            products = result.scalars().all()
            return [{
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'quantity': float(product.quantity),
                'created_at': product.created_at
            } for product in products]
    
    async def get_product(self, product_id):
        async with self.db.begin() as session:
            try:
                query = (
                    select(Product)
                    .where(Product.id == product_id)
                )
                result = await session.execute(query)
                return result.scalar()
            except Exception as e:
                await session.rollback()
                raise ValueError(f"Failed to create product: {str(e)}")
                
    
    async def create_product(self, product_data):
        async with self.db.begin() as session:  
            try:
                stmt = (
                    insert(Product)
                    .values(
                        id=product_data.get('id', uuid.uuid4()),  
                        name=product_data['name'],
                        price=product_data['price'],
                        quantity=product_data.get('quantity', 0),
                        created_at=product_data.get('created_at', datetime.utcnow())
                    )
                    .returning(Product)
                )
                
                result = await session.execute(stmt)
                created_product = result.scalar_one()
                
                return {
                    'id': created_product.id,
                    'name': created_product.name,
                    'price': float(created_product.price),
                    'quantity': float(created_product.quantity),  
                    'created_at': created_product.created_at.isoformat()
                }
                
            except Exception as e:
                await session.rollback()
                raise ValueError(f"Failed to create product: {str(e)}")

    async def patch_product(self, product_id: UUID, update_data: Dict[str, Any]) -> Dict[str, Any]:
        async with self.db.begin() as session:
            try:
    
                if not update_data:
                    raise ValueError("No update data provided")
                

                stmt = (
                    update(Product)
                    .where(Product.id == product_id)
                    .values(**update_data)
                    .returning(Product)
                )
                

                result = await session.execute(stmt)
                updated_product = result.scalar_one()
                

                return {
                    'id': updated_product.id,
                    'name': updated_product.name,
                    'price': float(updated_product.price),
                    'quantity': float(updated_product.quantity),
                    'created_at': updated_product.created_at.isoformat()
                }
            except Exception as e:
                await session.rollback()
                raise ValueError(f"Failed to patch product: {str(e)}")
    
    async def update_product(self, product_id: UUID, product_data: Dict[str, Any]) -> Dict[str, Any]:
        async with self.db.begin() as session:
            try:
                if not product_data:
                    raise ValueError("No product data provided for update")
                
                stmt = (
                    update(Product)
                    .where(Product.id == product_id)
                    .values(**product_data)
                    .returning(Product)
                )
                
    
                result = await session.execute(stmt)
                updated_product = result.scalar_one()
                

                return {
                    'id': updated_product.id,
                    'name': updated_product.name,
                    'price': float(updated_product.price),
                    'quantity': float(updated_product.quantity),
                    'created_at': updated_product.created_at.isoformat()
                }
                
            except Exception as e:
                await session.rollback()
                raise ValueError(f"Failed to update product: {str(e)}")
    
    async def delete_product(self, product_id: UUID) -> bool:
        async with self.db.begin() as session:
            try:
                stmt = (
                    delete(Product)
                    .where(Product.id == product_id)
                    .returning(Product.id)
                )
                

                result = await session.execute(stmt)
                deleted_product_id = result.scalar_one_or_none()
                
                if not deleted_product_id:
                    return False
    
                return True
                
            except Exception as e:
                await session.rollback()
                raise ValueError(f"Failed to delete product: {str(e)}")
    
    async def create_transaction_with_items(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        async with self.db.begin() as session:
            try:
                required_fields = ['cashier_id', 'total_price', 'items']
                for field in required_fields:
                    if field not in transaction_data:
                        raise ValueError(f"Missing required field: {field}")

                product_ids = [item['product_id'] for item in transaction_data['items']]
                products = await session.execute(
                    select(Product).where(Product.id.in_(product_ids))
                )
                products = products.scalars().all()
                product_map = {p.id: p for p in products}

                for item in transaction_data['items']:
                    if item['product_id'] not in product_map:
                        raise ValueError(f"Product {item['product_id']} not found")

                transaction_values = {
                    'id': transaction_data.get('id', uuid.uuid4()),
                    'cashier_id': transaction_data['cashier_id'],
                    'total_price': transaction_data['total_price'],
                    'status': transaction_data.get('status', 'paid'),
                    'created_at': transaction_data.get('created_at', datetime.utcnow()),
                    'updated_at': transaction_data.get('updated_at', datetime.utcnow())
                }
                
                stmt = insert(Transaction).values(**transaction_values).returning(Transaction)
                result = await session.execute(stmt)
                new_transaction = result.scalar_one()
                
                if transaction_data['items']:
                    items_values = [{
                        'transaction_id': new_transaction.id,
                        'product_id': item['product_id'],
                        'quantity': item['quantity']
                    } for item in transaction_data['items']]
                    
                    await session.execute(
                        insert(transaction_product).values(items_values)
                    )
                
                transaction_dict = {
                    'id': new_transaction.id,
                    'cashier_id': new_transaction.cashier_id,
                    'total_price': int(new_transaction.total_price),  
                    'status': new_transaction.status,
                    'created_at': new_transaction.created_at.isoformat(),
                    'updated_at': new_transaction.updated_at.isoformat(),
                    'items': [
                        {
                            'product_id': item['product_id'],
                            'name': product_map[item['product_id']].name,
                            'price': int(product_map[item['product_id']].price),  
                            'quantity': int(item['quantity'])  
                        } for item in transaction_data['items']
                    ]
                }
                return transaction_dict
            except Exception as e:
                await session.rollback()
                raise ValueError(f"Failed to create transaction: {str(e)}")

    async def get_transactions_with_items(
        self,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        async with self.db.begin() as session:
            stmt = (
                select(
                    Transaction,
                    Product,
                    transaction_product.c.quantity
                )
                .join(
                    transaction_product,
                    Transaction.id == transaction_product.c.transaction_id
                )
                .join(
                    Product,
                    Product.id == transaction_product.c.product_id
                )
                .order_by(Transaction.created_at.desc())
                .offset(skip)
                .limit(limit)
            )

            if start_date:
                stmt = stmt.where(Transaction.created_at >= start_date)
            if end_date:
                stmt = stmt.where(Transaction.created_at <= end_date)

            result = await session.execute(stmt)
            records = result.all()

            transactions_map = {}
            for transaction, product, quantity in records:
                if transaction.id not in transactions_map:
                    transactions_map[transaction.id] = {
                        "id": transaction.id,
                        "cashier_id": transaction.cashier_id,
                        "total_price": int(transaction.total_price),  
                        "status": transaction.status,
                        "created_at": transaction.created_at.isoformat(),
                        "updated_at": transaction.updated_at.isoformat(),
                        "items": []
                    }
                transactions_map[transaction.id]["items"].append({
                    "product_id": product.id,
                    "name": product.name,
                    "price": int(product.price),  
                    "quantity": int(quantity)  
                })

            return list(transactions_map.values())
    
    async def get_transaction_with_items(self, transaction_id: UUID):
        async with self.db.begin() as session:
            stmt = (
                select(
                    Transaction,
                    Product,
                    transaction_product.c.quantity
                )
                .join(
                    transaction_product,
                    Transaction.id == transaction_product.c.transaction_id
                )
                .join(
                    Product,
                    Product.id == transaction_product.c.product_id
                )
                .where(Transaction.id == transaction_id)
            )
            
            result = await session.execute(stmt)
            records = result.all()
            
            if not records:
                return None
                
            transaction = records[0][0]
            items = [{
                "product_id": product.id,
                "name": product.name,
                "price": int(product.price),  
                "quantity": int(quantity)     
            } for (_, product, quantity) in records]
            
            return {
                "id": transaction.id,
                "cashier_id": transaction.cashier_id,
                "total_price": int(transaction.total_price),  
                "status": transaction.status,
                "created_at": transaction.created_at.isoformat(),
                "updated_at": transaction.updated_at.isoformat(),
                "items": items
            }

    async def update_transaction(self, transaction_id: UUID, 
                        update_data: Dict[str, Any]) -> Dict[str, Any]:
        async with self.db.begin() as session:
            try:
                if not update_data:
                    raise ValueError("No transaction data provided for update")
                
                forbidden_fields = ['id', 'created_at']
                for field in forbidden_fields:
                    if field in update_data:
                        raise ValueError(f"Cannot update field: {field}")
                
                stmt = (
                    update(Transaction)
                    .where(Transaction.id == transaction_id)
                    .values(**update_data)
                    .returning(Transaction)
                )
                
                result = await session.execute(stmt)
                updated_transaction = result.scalar_one()
                
                items = await self.get_transaction_items(updated_transaction.id)
                
                return {
                    "id": updated_transaction.id,
                    "cashier_id": updated_transaction.cashier_id,
                    "total_price": int(updated_transaction.total_price),
                    "status": updated_transaction.status,
                    "created_at": updated_transaction.created_at.isoformat(),
                    "updated_at": updated_transaction.updated_at.isoformat(),
                    "items": items
                }
                
            except Exception as e:
                await session.rollback()
                raise ValueError(f"Failed to update transaction: {str(e)}")

    async def get_transaction_items(self, transaction_id: UUID) -> List[Dict[str, Any]]:
        async with self.db.begin() as session:
            stmt = (
                select(Product, transaction_product.c.quantity)
                .join(
                    transaction_product,
                    Product.id == transaction_product.c.product_id
                )
                .where(transaction_product.c.transaction_id == transaction_id)
            )
            result = await session.execute(stmt)
            return [{
                "product_id": product.id,
                "name": product.name,
                "price": int(product.price),
                "quantity": int(quantity)
            } for (product, quantity) in result.all()]

    async def delete_transaction(self, transaction_id: UUID) -> bool:
        async with self.db.begin() as session:
            try:
                await session.execute(
                    delete(transaction_product)
                    .where(transaction_product.c.transaction_id == transaction_id)
                )
                
                stmt = (
                    delete(Transaction)
                    .where(Transaction.id == transaction_id)
                    .returning(Transaction.id)
                )
                
                result = await session.execute(stmt)
                deleted_transaction_id = result.scalar_one_or_none()
                
                return deleted_transaction_id is not None
                
            except Exception as e:
                await session.rollback()
                raise ValueError(f"Failed to delete transaction: {str(e)}")
repository = Repository(async_session)