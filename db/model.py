from datetime import datetime
from sqlalchemy import (
    Column, String, DateTime, Integer, 
    ForeignKey, Table, Numeric, UUID
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ENUM
from enum import Enum as PyEnum
import uuid

Base = declarative_base()

transaction_product = Table(
    'transaction_product',
    Base.metadata,
    Column('transaction_id', UUID(as_uuid=True), ForeignKey('transactions.id'), primary_key=True),
    Column('product_id', UUID(as_uuid=True), ForeignKey('products.id'), primary_key=True),
    Column('quantity', Numeric(10, 2), nullable=False)  
)

class Product(Base):
    __tablename__ = 'products'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship(
        "Transaction",
        secondary=transaction_product,
        back_populates="products"
    )

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cashier_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False) 
    total_price = Column(Numeric(10, 2), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cashier = relationship("User", back_populates="transactions")
    products = relationship(
        "Product",
        secondary=transaction_product,
        back_populates="transactions"
    )

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="cashier")