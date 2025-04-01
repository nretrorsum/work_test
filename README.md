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

### POST /api/auth/login
Logs in a user and returns a JWT token in cookies.

Request Body:
```
{
  "username": "string",
  "password": "string"
}
```
Response:
```
Status: 200 OK
```
Returns a JWT token set as a cookie (access_token).

### POST /api/auth/logout
Logs out the user by clearing the JWT token cookie.

Response:

Status: 200 OK

Returns: A message confirming successful logout.

### GET /api/auth/me
Fetches the authenticated user's profile.

Response:
```
{
  "user_id": "string",
  "username": "string",
  "role": "admin" | "cashier"
}
```
Product Endpoints
### POST /api/product/add_product
Adds a new product to the system.

Request Body:
```
{
  "name": "string",
  "price": "number",
  "quantity": "number"
}
```
Response:
```
Status: 201 Created
```
Returns: The created product data.

### GET /api/product
Lists all products, with optional pagination.

Query Parameters:
```
skip (optional): Number of products to skip. Default is 0.

limit (optional): Number of products to return. Default is 100.
```
Response:
```
[
  {
    "id": "UUID",
    "name": "string",
    "price": "number",
    "quantity": "number",
    "created_at": "datetime"
  }
]
```
#GET /api/product/{product_id}
Fetches a single product by its ID.

Path Parameter:
```
product_id (required): The UUID of the product.
```
Response:
```
{
  "id": "UUID",
  "name": "string",
  "price": "number",
  "quantity": "number",
  "created_at": "datetime"
}
```
### PUT /api/product/update_product/{product_id}
Updates an existing product.

Path Parameter:
```
product_id (required): The UUID of the product.
```
Request Body:
```
{
  "name": "string",
  "price": "number",
  "quantity": "number"
}
```
Response:
```
{
  "id": "UUID",
  "name": "string",
  "price": "number",
  "quantity": "number",
  "created_at": "datetime"
}
```
### PATCH /api/product/patch_product/{product_id}
Partially updates an existing product.

Path Parameter:
```
product_id (required): The UUID of the product.
```
Request Body:
```
{
  "name": "string",
  "price": "number",
  "quantity": "number"
}
```
Response:
```
{
  "id": "UUID",
  "name": "string",
  "price": "number",
  "quantity": "number",
  "created_at": "datetime"
}
```
Transaction Endpoints
### POST /transactions
Creates a new transaction with products.

Request Body:
```
{
  "cashier_id": "UUID",
  "total_price": "number",
  "status": "string",
  "items": [
    {
      "product_id": "UUID",
      "quantity": "number",
      "price": "number"
    }
  ]
}
```
Response:
```
{
  "id": "UUID",
  "cashier_id": "UUID",
  "total_price": "number",
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```
### GET /transactions
Lists all transactions, with optional filtering and pagination.

Query Parameters:
```
skip (optional): Number of transactions to skip. Default is 0.

limit (optional): Number of transactions to return. Default is 100.

start_date (optional): Start date for filtering transactions.

end_date (optional): End date for filtering transactions.
```
Response:
```
[
  {
    "id": "UUID",
    "cashier_id": "UUID",
    "total_price": "number",
    "status": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```
### GET /transactions/{transaction_id}
Fetches a single transaction by its ID.

Path Parameter:
```
transaction_id (required): The UUID of the transaction.
```
Response:
```
{
  "id": "UUID",
  "cashier_id": "UUID",
  "total_price": "number",
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```
### PATCH /transactions/{transaction_id}
Partially updates an existing transaction.

Path Parameter:
```
transaction_id (required): The UUID of the transaction.
```
Request Body:
```
{
  "cashier_id": "UUID",
  "total_price": "number",
  "status": "string"
}
```
Response:
```
{
  "id": "UUID",
  "cashier_id": "UUID",
  "total_price": "number",
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```
### DELETE /transactions/{transaction_id}
Deletes a transaction.

Path Parameter:
```
transaction_id (required): The UUID of the transaction.
```
Response:
```
{
  "message": "Transaction deleted successfully"
}
```
Error Handling
All endpoints support the following HTTP status codes for error handling:
```
400 Bad Request: Invalid request data.

401 Unauthorized: Invalid authentication or login required.

403 Forbidden: User does not have permission to access the resource.

404 Not Found: Resource not found.

500 Internal Server Error: Unexpected server error.
```