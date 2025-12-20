# API Usage Guide

This guide provides detailed examples for interacting with the E-commerce Backend API.

## Base URL

```
http://127.0.0.1:8000
```

## Table of Contents

- [Products API](#products-api)
- [Product Query Options](#product-query-options)
- [Product Reviews](#product-reviews)
- [Collections API](#collections-api)
- [Carts](#carts)
- [Cart Items](#cart-items)
- [Customers](#customers)
- [Authentication (JWT)](#authentication-jwt)
- [Common Response Codes](#common-response-codes)
- [Error Handling](#error-handling)

---

## Products API

### 1. List All Products

**Endpoint:** `GET /store/products/`

**Permissions:** Read is open; create/update/delete require staff (admin) accounts.

**Request:**

```bash
curl http://127.0.0.1:8000/store/products/
```

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "Gaming Laptop",
    "description": "High-performance gaming laptop with RTX 3080",
    "price": "1499.99",
    "inventory": 25,
    "collection": 2,
    "price_with_tax": "1799.99"
  },
  {
    "id": 2,
    "title": "Wireless Mouse",
    "description": "Ergonomic wireless mouse",
    "price": "29.99",
    "inventory": 150,
    "collection": 3,
    "price_with_tax": "35.99"
  }
]
```

---

### 2. Get Single Product

**Endpoint:** `GET /store/products/{id}/`

**Request:**

```bash
curl http://127.0.0.1:8000/store/products/1/
```

**Response:** `200 OK`

```json
{
  "id": 1,
  "title": "Gaming Laptop",
  "description": "High-performance gaming laptop with RTX 3080",
  "price": "1499.99",
  "inventory": 25,
  "collection": 2,
  "price_with_tax": "1799.99"
}
```

**Error Response:** `404 Not Found`

```json
{
  "detail": "Not found."
}
```

---

### 3. Create New Product

**Endpoint:** `POST /store/products/`

**Request:**

```bash
curl -X POST http://127.0.0.1:8000/store/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mechanical Keyboard",
    "description": "RGB mechanical keyboard with blue switches",
    "price": "89.99",
    "inventory": 75,
    "collection": 3
  }'
```

**Response:** `201 Created`

```json
{
  "id": 15,
  "title": "Mechanical Keyboard",
  "description": "RGB mechanical keyboard with blue switches",
  "price": "89.99",
  "inventory": 75,
  "collection": 3,
  "price_with_tax": "107.99"
}
```

**Validation Error:** `400 Bad Request`

```json
{
  "price": ["A valid number is required."],
  "collection": ["This field is required."]
}
```

---

### 4. Update Product (Full Update)

**Endpoint:** `PUT /store/products/{id}/`

**Request:**

```bash
curl -X PUT http://127.0.0.1:8000/store/products/15/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mechanical Keyboard Pro",
    "description": "Professional RGB mechanical keyboard with blue switches",
    "price": "99.99",
    "inventory": 80,
    "collection": 3
  }'
```

**Response:** `200 OK`

```json
{
  "id": 15,
  "title": "Mechanical Keyboard Pro",
  "description": "Professional RGB mechanical keyboard with blue switches",
  "price": "99.99",
  "inventory": 80,
  "collection": 3,
  "price_with_tax": "119.99"
}
```

**Note:** PUT requires all fields to be provided.

---

### 5. Update Product (Partial Update)

**Endpoint:** `PATCH /store/products/{id}/`

**Request:**

```bash
curl -X PATCH http://127.0.0.1:8000/store/products/15/ \
  -H "Content-Type: application/json" \
  -d '{
    "price": "79.99",
    "inventory": 100
  }'
```

**Response:** `200 OK`

```json
{
  "id": 15,
  "title": "Mechanical Keyboard Pro",
  "description": "Professional RGB mechanical keyboard with blue switches",
  "price": "79.99",
  "inventory": 100,
  "collection": 3,
  "price_with_tax": "95.99"
}
```

**Note:** PATCH allows updating only specific fields.

---

### 6. Delete Product

**Endpoint:** `DELETE /store/products/{id}/`

**Request:**

```bash
curl -X DELETE http://127.0.0.1:8000/store/products/15/
```

**Successful Response:** `204 No Content`
(No response body)

**Protected Resource:** `405 Method Not Allowed`

```json
{
  "error": "Product cannot be deleted because it is associated with an order item."
}
```

**Note:** Products cannot be deleted if they are part of any order.

---

## Product Query Options

- **Filter**
  - By collection: `/store/products/?collection_id=3`
  - By price range: `/store/products/?price__gt=50&price__lt=200`
- **Search**
  - `/store/products/?search=keyboard` (matches `title`, `description`)
- **Ordering**
  - `/store/products/?ordering=price` or `/store/products/?ordering=-title`
- **Pagination** (page-number)
  - `/store/products/?page=2&page_size=20` (max `page_size` is 100)

Combine them as needed, for example:

```bash
curl "http://127.0.0.1:8000/store/products/?collection_id=3&search=mouse&ordering=-price&page=1&page_size=5"
```

---

## Collections API

### 1. List All Collections

**Endpoint:** `GET /store/collections/`

**Permissions:** Read is open; create/update/delete require staff (admin) accounts.

**Request:**

```bash
curl http://127.0.0.1:8000/store/collections/
```

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "Electronics"
  },
  {
    "id": 2,
    "title": "Laptops"
  },
  {
    "id": 3,
    "title": "Accessories"
  }
]
```

---

### 2. Get Single Collection

**Endpoint:** `GET /store/collections/{pk}/`

**Request:**

```bash
curl http://127.0.0.1:8000/store/collections/1/
```

**Response:** `200 OK`

```json
{
  "id": 1,
  "title": "Electronics"
}
```

---

### 3. Create New Collection

**Endpoint:** `POST /store/collections/`

**Request:**

```bash
curl -X POST http://127.0.0.1:8000/store/collections/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Gaming Gear"
  }'
```

**Response:** `201 Created`

```json
{
  "id": 5,
  "title": "Gaming Gear"
}
```

---

### 4. Update Collection (Full)

**Endpoint:** `PUT /store/collections/{pk}/`

**Request:**

```bash
curl -X PUT http://127.0.0.1:8000/store/collections/5/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Gaming Peripherals"
  }'
```

**Response:** `200 OK`

```json
{
  "id": 5,
  "title": "Gaming Peripherals"
}
```

---

### 5. Update Collection (Partial)

**Endpoint:** `PATCH /store/collections/{pk}/`

**Request:**

```bash
curl -X PATCH http://127.0.0.1:8000/store/collections/5/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Pro Gaming"
  }'
```

**Response:** `200 OK`

```json
{
  "id": 5,
  "title": "Pro Gaming"
}
```

---

### 6. Delete Collection

**Endpoint:** `DELETE /store/collections/{pk}/`

**Request:**

```bash
curl -X DELETE http://127.0.0.1:8000/store/collections/5/
```

**Successful Response:** `204 No Content`

**Protected Resource:** `405 Method Not Allowed`

```json
{
  "error": "Collection cannot be deleted because it includes one or more products."
}
```

**Note:** Collections cannot be deleted if they contain any products.

---

## Product Reviews

Nested under a product using `product_id`.

### 1. List Reviews

`GET /store/products/{product_id}/reviews/`

```bash
curl http://127.0.0.1:8000/store/products/1/reviews/
```

### 2. Create Review

`POST /store/products/{product_id}/reviews/`

```bash
curl -X POST http://127.0.0.1:8000/store/products/1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane", "description": "Great value"}'
```

### 3. Update / Delete Review

Use `PUT`, `PATCH`, or `DELETE` on `/store/products/{product_id}/reviews/{id}/`.

---

## Carts

### 1. Create Cart

`POST /store/carts/`

```bash
curl -X POST http://127.0.0.1:8000/store/carts/
```

Response returns a cart UUID: `{ "id": "<cart_id>", "items": [], "total_price": "0.00" }`

### 2. Get Cart

`GET /store/carts/{cart_id}`

Returns cart lines with `total_price` aggregated.

### 3. Delete Cart

`DELETE /store/carts/{cart_id}` deletes the cart and all items.

---

## Cart Items

Nested under a cart using `cart_id`.

### 1. Add Item

`POST /store/carts/{cart_id}/items/`

```bash
curl -X POST http://127.0.0.1:8000/store/carts/abcd1234/items/ \
  -H "Content-Type: application/json" \
  -d '{"product_id": 3, "quantity": 2}'
```

- If the product already exists in the cart, quantity is incremented.

### 2. List Items

`GET /store/carts/{cart_id}/items/`

### 3. Update Quantity

`PATCH /store/carts/{cart_id}/items/{id}` with `{ "quantity": 5 }`.

### 4. Remove Item

`DELETE /store/carts/{cart_id}/items/{id}`

---

## Customers

- Admin-only CRUD: `/store/customers/` and `/store/customers/{id}`
- Authenticated self-service endpoint:

  - `GET /store/customers/me/` — fetch your profile
  - `PUT /store/customers/me/` — update your profile (phone, birth_date, membership)

---

## Authentication (JWT)

Provided by Djoser + Simple JWT.

### Endpoints

| Method | Endpoint             | Description                   |
| ------ | -------------------- | ----------------------------- |
| POST   | `/auth/jwt/create/`  | Obtain `access` and `refresh` |
| POST   | `/auth/jwt/refresh/` | Refresh the `access` token    |
| POST   | `/auth/jwt/verify/`  | Verify token validity         |
| POST   | `/auth/users/`       | Register user                 |
| GET    | `/auth/users/me/`    | Current user profile          |

### Request examples

Create tokens:

```bash
curl -X POST http://127.0.0.1:8000/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "your-password"}'
```

Use access token (header type set to `JWT` in settings):

```bash
curl http://127.0.0.1:8000/store/products/ \
  -H "Authorization: JWT <access_token>"
```

Refresh token:

```bash
curl -X POST http://127.0.0.1:8000/auth/jwt/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

Verify token:

```bash
curl -X POST http://127.0.0.1:8000/auth/jwt/verify/ \
  -H "Content-Type: application/json" \
  -d '{"token": "<access_or_refresh>"}'
```

**Authorization header**: `Authorization: JWT <access_token>`

---

## Common Response Codes

| Status Code               | Meaning              | When It Happens                   |
| ------------------------- | -------------------- | --------------------------------- |
| 200 OK                    | Success              | GET, PUT, PATCH successful        |
| 201 Created               | Resource created     | POST successful                   |
| 204 No Content            | Deleted successfully | DELETE successful                 |
| 400 Bad Request           | Validation error     | Invalid data provided             |
| 404 Not Found             | Resource not found   | Invalid ID/resource doesn't exist |
| 405 Method Not Allowed    | Action not allowed   | Protected resource deletion       |
| 500 Internal Server Error | Server error         | Unexpected server issue           |

---

## Error Handling

### Validation Errors (400)

When you send invalid data:

```json
{
  "title": ["This field is required."],
  "price": ["Ensure this value is greater than or equal to 0."],
  "inventory": ["A valid integer is required."]
}
```

### Not Found (404)

When a resource doesn't exist:

```json
{
  "detail": "Not found."
}
```

### Business Logic Errors (405)

When trying to delete protected resources:

```json
{
  "error": "Product cannot be deleted because it is associated with an order item."
}
```

---

## Using with Tools

### Postman

1. Set method (GET, POST, PUT, PATCH, DELETE)
2. Enter URL: `http://127.0.0.1:8000/store/products/`
3. For POST/PUT/PATCH:
   - Set Headers: `Content-Type: application/json`
   - Add JSON body in Body tab (raw)
4. Send request

### cURL

All examples above use cURL. Key flags:

- `-X METHOD` - Specify HTTP method
- `-H "Header: Value"` - Add headers
- `-d 'data'` - Request body

### Python Requests

```python
import requests

# GET request
response = requests.get('http://127.0.0.1:8000/store/products/')
products = response.json()

# POST request
data = {
    "title": "New Product",
    "description": "Description here",
    "price": "49.99",
    "inventory": 100,
    "collection": 1
}
response = requests.post(
    'http://127.0.0.1:8000/store/products/',
    json=data
)
created_product = response.json()

# PATCH request
update_data = {"price": "39.99"}
response = requests.patch(
    'http://127.0.0.1:8000/store/products/1/',
    json=update_data
)

# DELETE request
response = requests.delete('http://127.0.0.1:8000/store/products/1/')
```

---

## Tips

1. **Always check response status codes** to understand what happened
2. **Use PATCH for partial updates** instead of PUT when you only need to change a few fields
3. **Handle 404 errors gracefully** in your client application
4. **Respect business logic rules** - check for 405 errors on deletion
5. **Validate data client-side** before sending to reduce 400 errors
6. **Use Django Debug Toolbar** during development to monitor query performance

---

## Next Steps

- Add authentication headers when auth is implemented
- Implement pagination for large result sets
- Add filtering and searching capabilities
- Explore additional endpoints (tags, likes, playground)

For more details, see the main [README.md](README.md).
