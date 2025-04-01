# Store Management System API Documentation

## Overview
A FastAPI-based system for managing store operations with:

### Key Features
- **User Authentication**: Registration, login, logout
- **Product Management**: Full CRUD operations
- **Transaction Processing**: Create and manage sales
- **Role-Based Access**: Admin and cashier roles

### Technology Stack
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: JWT tokens
- **Validation**: Pydantic models

---

## API Endpoints

Authentication
POST /api/auth/register
Description: Register a new user

Request Body:


{
  "username": "string",
  "password": "string",
  "role": "admin" | "cashier"
}
Response:


{
  "status": "201",
  "detail": "user created"
}
POST /api/auth/login
Description: Login user and set JWT cookie

Request Body:


{
  "username": "string",
  "password": "string"
}
Response:


{
  "status": "200",
  "detail": "Authenticated"
}
Sets Cookie: access_token with JWT

POST /api/auth/logout
Description: Logout user by clearing JWT cookie

Response:


{
  "status": "200",
  "detail": "Successfully logged out"
}
GET /api/auth/me
Description: Get current user profile

Requires Authentication: Yes (JWT cookie)

Response:


{
  "user_id": "uuid",
  "username": "string",
  "role": "string"
}
Products
POST /api/product/add_product
Description: Add a new product

Requires Authentication: Yes (admin role)

Request Body:


{
  "name": "string",
  "price": integer,
  "quantity": integer
}
Response:


{
  "id": "uuid",
  "name": "string",
  "price": float,
  "quantity": float,
  "created_at": "datetime"
}
GET /api/product/
Description: List all products with pagination

Query Parameters:

skip: integer (default 0)

limit: integer (default 100)

Response:


[
  {
    "id": "uuid",
    "name": "string",
    "price": float,
    "quantity": float,
    "created_at": "datetime"
  }
]
GET /api/product/{product_id}
Description: Get product details by ID

Response:


{
  "id": "uuid",
  "name": "string",
  "price": float,
  "quantity": float,
  "created_at": "datetime"
}
PUT /api/product/update_product/{product_id}
Description: Fully update a product

Requires Authentication: Yes (admin role)

Request Body:


{
  "name": "string",
  "price": integer,
  "quantity": integer
}
Response:


{
  "id": "uuid",
  "name": "string",
  "price": float,
  "quantity": float,
  "created_at": "datetime"
}
PATCH /api/product/patch_product/{product_id}
Description: Partially update a product

Requires Authentication: Yes (admin role)

Request Body:


{
  "name": "string (optional)",
  "price": "integer (optional)",
  "quantity": "integer (optional)"
}
Response:


{
  "id": "uuid",
  "name": "string",
  "price": float,
  "quantity": float,
  "created_at": "datetime"
}
Transactions
POST /transactions/
Description: Create a new transaction with items

Requires Authentication: Yes (cashier role)

Request Body:


{
  "cashier_id": "uuid",
  "total_price": integer,
  "status": "paid" | "canceled",
  "items": [
    {
      "product_id": "uuid",
      "quantity": integer
    }
  ]
}
Response:


{
  "id": "uuid",
  "cashier_id": "uuid",
  "total_price": integer,
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "items": [
    {
      "product_id": "uuid",
      "name": "string",
      "price": integer,
      "quantity": integer
    }
  ]
}
GET /transactions/
Description: List transactions with optional date filtering

Query Parameters:

skip: integer (default 0)

limit: integer (default 100)

start_date: datetime (optional)

end_date: datetime (optional)

Response:


[
  {
    "id": "uuid",
    "cashier_id": "uuid",
    "total_price": integer,
    "status": "string",
    "created_at": "datetime",
    "updated_at": "datetime",
    "items": [
      {
        "product_id": "uuid",
        "name": "string",
        "price": integer,
        "quantity": integer
      }
    ]
  }
]
GET /transactions/{transaction_id}
Description: Get transaction details by ID

Response:


{
  "id": "uuid",
  "cashier_id": "uuid",
  "total_price": integer,
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "items": [
    {
      "product_id": "uuid",
      "name": "string",
      "price": integer,
      "quantity": integer
    }
  ]
}
PATCH /transactions/{transaction_id}
Description: Update transaction details

Request Body:


{
  "cashier_id": "uuid (optional)",
  "total_price": "integer (optional)",
  "status": "string (optional)"
}
Response:


{
  "id": "uuid",
  "cashier_id": "uuid",
  "total_price": integer,
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "items": [
    {
      "product_id": "uuid",
      "name": "string",
      "price": integer,
      "quantity": integer
    }
  ]
}
DELETE /transactions/{transaction_id}
Description: Delete a transaction

Response:


{
  "message": "Transaction deleted successfully"
}
Database Schema
The system uses the following main tables:

users: Stores user accounts with roles

products: Stores product information

transactions: Records sales transactions

transaction_product: Junction table for transaction items

Error Responses
All endpoints return standardized error responses:

400 Bad Request: Invalid input data

401 Unauthorized: Missing or invalid authentication

404 Not Found: Resource not found

500 Internal Server Error: Server-side error

Error response format:


{
  "detail": "Error message"
}