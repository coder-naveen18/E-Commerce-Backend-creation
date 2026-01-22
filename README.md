# E-commerce Backend API

A comprehensive Django REST Framework-based backend system for an e-commerce platform. This project provides a complete set of RESTful APIs for managing products, collections, customers, orders, carts, and more.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Email Verification](#email-verification)
- [Data Population](#data-population)
- [API Documentation](#api-documentation)

## ✨ Features

- **Product Management**: Full CRUD with pricing, inventory, descriptions, and per-product image gallery (500 KB max per image)
- **Collection Management**: Organize products into collections with featured products
- **Customer Management**: Track customer information with membership tiers (Gold, Silver, Bronze)
- **Catalog Discovery**: Filtering (collection, price range), search (title, description), ordering (title, price), and page-number pagination
- **Order Management**: Create orders from an existing cart via `cart_id`; payment status lifecycle (Pending/Confirm/Failed) and `order_created` signal hook
- **Shopping Cart**: Hex-based cart IDs, cart item management, and quantity merging
- **Product Reviews**: Nested reviews per product with clean URL structure
- **Product Media**: Nested image upload endpoint under products with size validation and media storage
- **Customer Profile Endpoint**: `customers/me/` for authenticated self-service profile read/update
- **Authentication**: JWT auth via Djoser + Simple JWT (`/auth/jwt/create`, `/auth/jwt/refresh`, `/auth/jwt/verify`)
- **Email Verification**: Token-based email verification with 48-hour expiry; orders blocked until email verified
- **Promotion System**: Apply promotions and discounts to products
- **Address Management**: One-to-one relationship for customer addresses
- **Phone Number Support**: International phone number validation using phonenumber_field
- **Optimized Queries**: Uses `select_related()`/`prefetch_related()` to prevent N+1 query problems
- **Background Tasks**: Celery-ready with Redis broker and sample notification task
- **CORS + Media**: CORS origins configurable via environment; media served from `/media/`
- **Protection Rules**: Prevents deletion of products/collections associated with orders

## 🛠 Tech Stack

- **Framework**: Django 6.0+
- **API**: Django REST Framework
- **Database**: Configurable via environment (tested with MySQL; SQLite/PostgreSQL ready)
- **Utilities**:
  - `django-extensions` - Additional management commands
  - `django-debug-toolbar` - Performance debugging
  - `django-filter` - Query filtering for list endpoints
  - `drf-nested-routers` - Nested routing for cart items, product reviews, and product images
  - `djoser` + `djangorestframework-simplejwt` - Auth endpoints and JWT issuance/refresh/verify
  - `phonenumber_field` - International phone number validation
  - `python-dotenv` - Environment variable management
  - `django-cors-headers` - CORS handling
  - `celery` + Redis (broker) - Background task execution
  - `Pillow` - Image handling for product media

## 📁 Project Structure

```
E-commerce Backend/
│
├── Ecommerce/              # Main project configuration
│   ├── settings.py         # Project settings
│   ├── urls.py             # Root URL configuration
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
│
├── store/                  # Main store application
│   ├── models.py           # Database models
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # API views (ViewSets)
│   ├── urls.py             # Store URL routes
│   ├── admin.py            # Admin interface configuration
│   ├── signals.py          # Django signals (auto Customer creation)
│   ├── apps.py             # App configuration (registers signals)
│   └── migrations/         # Database migrations
│
├── likes/                  # Likes functionality app
├── tags/                   # Tags functionality app
├── playground/             # Testing/experimental app
├── core/                   # core store extensions
│
├── manage.py               # Django management script
├── db.sqlite3              # SQLite database
├── populate_cart_data.py   # Script to populate cart data
└── .env                    # Environment variables (not in repo)
```

## 🗄 Database Models

### User (Custom)

Custom user model extending Django's AbstractUser with unique email requirement.

```python
- username: CharField (inherited, unique)
- email: EmailField (unique, required)
- email_verified: BooleanField (default=False)
- email_verification_token: CharField (32-char hex, nullable)
- token_created_at: DateTimeField (nullable)
- first_name: CharField (inherited)
- last_name: CharField (inherited)
- password: CharField (inherited, hashed)
```

**Auth Model**: Set as `AUTH_USER_MODEL = 'core.User'` in settings.

### Product

Core product model with pricing, inventory tracking, and relationships.

```python
- title: CharField(max_length=255)
- description: TextField
- price: DecimalField (with MinValueValidator(0))
- inventory: IntegerField (with MinValueValidator(0))
- last_update: DateTimeField (auto_now)
- collection: ForeignKey to Collection
- promotions: ManyToManyField to Promotion
```

### ProductImage

Per-product media with validation and optional alt text.

```python
- product: ForeignKey to Product (CASCADE)
- image: ImageField (uploads to `media/store/images/`, max 500 KB)
- alt_text: CharField(max_length=255, optional)
```

### Collection

Product categorization with optional featured product.

```python
- title: CharField(max_length=255)
- featured_product: ForeignKey to Product (nullable)
```

### Customer

Customer information with membership tiers. Automatically created when a new User registers.

```python
- user: OneToOneField to AUTH_USER_MODEL (CASCADE)
- phone: PhoneNumberField (optional)
- birth_date: DateField (optional)
- membership: CharField (Gold/Silver/Bronze, default: Silver)
```

**Note**: Customer profiles are automatically created via Django signals when a new User is registered through `/auth/users/`.

### Order

Order tracking with payment status.

```python
- payment_status: CharField (Pending/Confirm/Failed)
- placed_at: DateTimeField (auto_now_add)
- customer: ForeignKey to Customer
```

### OrderItem

Individual items within an order.

```python
- order: ForeignKey to Order
- product: ForeignKey to Product (PROTECT)
- quantity: PositiveSmallIntegerField
- unit_price: DecimalField
```

### Cart & CartItem

Shopping cart functionality.

```python
Cart:
- id: CharField(primary_key, 32-char hex, no hyphens)
- created_at: DateTimeField(auto_now_add)

CartItem:
- cart: ForeignKey to Cart (CASCADE)
- product: ForeignKey to Product (CASCADE)
- quantity: PositiveSmallIntegerField
# unique_together on (cart, product) to merge quantities
```

### Address

Customer shipping/billing addresses (one-to-one with Customer).

```python
- zip_code: PositiveSmallIntegerField
- street: CharField(max_length=255)
- city: CharField(max_length=255)
- customer: OneToOneField to Customer (primary_key)
```

### Promotion

Promotional campaigns and discounts.

```python
- description: TextField
- discount: FloatField
```

## 🌐 API Endpoints

### Authentication (Djoser + Simple JWT)

| Method | Endpoint                      | Description                      |
| ------ | ----------------------------- | -------------------------------- |
| POST   | `/auth/jwt/create/`           | Obtain access/refresh tokens     |
| POST   | `/auth/jwt/refresh/`          | Refresh access token             |
| POST   | `/auth/jwt/verify/`           | Verify access or refresh token   |
| POST   | `/auth/users/`                | Register user                    |
| GET    | `/auth/users/me/`             | Get current user                 |
| POST   | `/auth/token/login/`          | Obtain DRF token (if enabled)    |
| POST   | `/auth/token/logout/`         | Revoke DRF token (if enabled)    |
| GET    | `/core/verify-email/{token}/` | Verify email address with token  |

**Authorization header**: `Authorization: JWT <access_token>` (matches `AUTH_HEADER_TYPES=('JWT',)` in settings)

**Email Verification Flow**:
1. User registers via `/auth/users/` → Verification email sent automatically
2. User clicks email link → Redirects to `/core/verify-email/{token}/`
3. Backend verifies token (48-hour expiry) → Sets `email_verified=True`
4. User can now place orders (blocked until verified)

### Products

| Method | Endpoint                | Description                 |
| ------ | ----------------------- | --------------------------- |
| GET    | `/store/products/`      | List all products           |
| POST   | `/store/products/`      | Create a new product        |
| GET    | `/store/products/{id}/` | Retrieve a specific product |
| PUT    | `/store/products/{id}/` | Update a product (full)     |
| PATCH  | `/store/products/{id}/` | Update a product (partial)  |
| DELETE | `/store/products/{id}/` | Delete a product\*          |

\*Deletion is prevented if the product is associated with any order items.

**Query parameters**

- Filtering: `collection_id`, `price__gt`, `price__lt`
- Search: `search` (matches `title`, `description`)
- Ordering: `ordering=title` or `ordering=price` (prefix with `-` for descending)
- Pagination: `page` and `page_size` (max 100)

### Collections

| Method | Endpoint                   | Description                    |
| ------ | -------------------------- | ------------------------------ |
| GET    | `/store/collections/`      | List all collections           |
| POST   | `/store/collections/`      | Create a new collection        |
| GET    | `/store/collections/{pk}/` | Retrieve a specific collection |
| PUT    | `/store/collections/{pk}/` | Update a collection (full)     |
| PATCH  | `/store/collections/{pk}/` | Update a collection (partial)  |
| DELETE | `/store/collections/{pk}/` | Delete a collection\*          |

\*Deletion is prevented if the collection contains any products.

### Product Reviews (nested)

| Method | Endpoint                                    | Description            |
| ------ | ------------------------------------------- | ---------------------- |
| GET    | `/store/products/{product_id}/reviews/`     | List reviews           |
| POST   | `/store/products/{product_id}/reviews/`     | Create review          |
| GET    | `/store/products/{product_id}/reviews/{id}` | Retrieve single review |
| PUT    | `/store/products/{product_id}/reviews/{id}` | Update review          |
| PATCH  | `/store/products/{product_id}/reviews/{id}` | Partial update         |
| DELETE | `/store/products/{product_id}/reviews/{id}` | Delete review          |

### Product Images (nested)

| Method | Endpoint                                    | Description                        |
| ------ | ------------------------------------------- | ---------------------------------- |
| GET    | `/store/products/{product_id}/images/`      | List all images for a product      |
| POST   | `/store/products/{product_id}/images/`      | Upload image (multipart form-data) |
| DELETE | `/store/products/{product_id}/images/{id}/` | Delete an image                    |

**Notes**

- Max file size: 500 KB (validation error otherwise)
- Upload path: `media/store/images/`

### Carts

| Method | Endpoint            | Description                          |
| ------ | ------------------- | ------------------------------------ |
| POST   | `/store/carts/`     | Create a cart (returns cart UUID)    |
| GET    | `/store/carts/{id}` | Retrieve cart with aggregated totals |
| DELETE | `/store/carts/{id}` | Delete cart and its items            |

**Notes**

- Cart IDs are 32-character hex strings (no hyphens). Keep the returned ID for subsequent item/order operations.

### Cart Items (nested)

| Method | Endpoint                            | Description                  |
| ------ | ----------------------------------- | ---------------------------- |
| GET    | `/store/carts/{cart_id}/items/`     | List items in cart           |
| POST   | `/store/carts/{cart_id}/items/`     | Add item (merges quantities) |
| PATCH  | `/store/carts/{cart_id}/items/{id}` | Update item quantity         |
| DELETE | `/store/carts/{cart_id}/items/{id}` | Remove item from cart        |

### Orders

| Method | Endpoint              | Description                                 |
| ------ | --------------------- | ------------------------------------------- |
| GET    | `/store/orders/`      | List orders (users see own; admins see all) |
| POST   | `/store/orders/`      | Create order from an existing cart          |
| GET    | `/store/orders/{id}/` | Retrieve order (admin or order owner)       |
| PATCH  | `/store/orders/{id}/` | Update order status (admin only)            |
| DELETE | `/store/orders/{id}/` | Delete order (admin only)                   |

**Create Order Payload**

```json
{
  "cart_id": "<32-char-hex-cart-id>"
}
```

**Requirements:**
- Requires authentication (JWT)
- **Email must be verified** (returns 403 if not)
- Cart must exist and contain items
- Copies items from cart into order, then deletes cart
- Emits an `order_created` signal for downstream listeners

### Customers

| Method | Endpoint                | Description                                  |
| ------ | ----------------------- | -------------------------------------------- |
| GET    | `/store/customers/`     | List customers (admin only)                  |
| POST   | `/store/customers/`     | Create customer (admin only)                 |
| GET    | `/store/customers/{id}` | Retrieve customer (admin only)               |
| PUT    | `/store/customers/{id}` | Update customer (admin only)                 |
| PATCH  | `/store/customers/{id}` | Partial update (admin only)                  |
| DELETE | `/store/customers/{id}` | Delete customer (admin only)                 |
| GET    | `/store/customers/me/`  | Get current authenticated customer's data    |
| PUT    | `/store/customers/me/`  | Update current authenticated customer's data |

**Note**: In the current implementation, `GET` on `/store/customers/` is open, while write operations require authentication. Adjust `CustomerViewSet.get_permissions` if stricter access is desired.

### Additional Endpoints

- `/tags/` - Tag management
- `/likes/` - Like functionality
- `/playground/` - Testing endpoints
- `/admin/` - Django Admin interface

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Setup

1. **Clone the repository**

   ```bash
   cd "C:\Users\coder\Desktop\E-commerce Backend"
   ```

2. **Create and activate virtual environment**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**

   ```powershell
    pip install django djangorestframework djangorestframework-simplejwt djoser django-filter django-extensions django-debug-toolbar drf-nested-routers phonenumber_field python-dotenv mysqlclient
    pip install -r requirements.txt
    pip install django-cors-headers celery redis Pillow  # extras referenced in settings/code
   ```

4. **Create `.env` file**

   Minimal (SQLite):

   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_ENGINE=django.db.backends.sqlite3
   DB_NAME=db.sqlite3
   CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
   
   # Email Settings (Console Backend - for development)
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   
   # For real email sending (Gmail example):
   # EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   # EMAIL_HOST=smtp.gmail.com
   # EMAIL_HOST_USER=your-email@gmail.com
   # EMAIL_HOST_PASSWORD=your-16-char-app-password
   # EMAIL_PORT=587
   # EMAIL_USE_TLS=True
   # DEFAULT_FROM_EMAIL=your-email@gmail.com
   # FRONTEND_URL=http://localhost:3000
   ```

   MySQL example:

   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_ENGINE=django.db.backends.mysql
   DB_NAME=ecommerce_db
   DB_USER=ecommerce
   DB_PASSWORD=secure-password
   DB_HOST=localhost
   DB_PORT=3306
   CORS_ALLOWED_ORIGINS=http://localhost:3000
   
   # Email Settings (SMTP)
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   DEFAULT_FROM_EMAIL=your-email@gmail.com
   FRONTEND_URL=http://localhost:3000
   ```

5. **Run migrations**

   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```powershell
   python manage.py createsuperuser
   ```

## ⚙ Configuration

### Environment Variables

Key variables pulled from `.env`:

- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
- `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- `CORS_ALLOWED_ORIGINS` (comma-separated origins)
- `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL`
- `FRONTEND_URL` (for email verification links)
- `VERIFICATION_TOKEN_EXPIRY` (token expiry in hours, default: 48)

### Database Configuration

The project uses SQLite by default. To use PostgreSQL or MySQL, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🏃 Running the Project

### Development Server

```powershell
python manage.py runserver
```

Access the application at:

- API: `http://127.0.0.1:8000/store/`
- Admin Panel: `http://127.0.0.1:8000/admin/`
- Debug Toolbar: Automatically appears in DEBUG mode

### Run with specific port

```powershell
python manage.py runserver 8080
```

### Background workers (Celery)

Requires a running Redis broker (`redis://localhost:6379/1` by default).

```powershell
# Windows - use solo pool to avoid multiprocessing issues
celery -A Ecommerce worker --pool=solo -l info
celery -A Ecommerce beat -l info
```

## 📧 Email Verification

### Overview

The system implements token-based email verification to ensure users confirm their email addresses before placing orders.

**Flow:**
1. User registers → Automatic verification email sent (via Celery)
2. User clicks email link → Backend verifies token
3. Token valid (within 48 hours) → Email marked verified
4. User can now place orders

### Setup Email (Development)

**Console Backend** (emails printed to terminal, no real sending):
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**Gmail SMTP** (sends real emails):

1. **Enable 2-Step Verification** on your Gmail account:
   - Go to https://myaccount.google.com/security
   - Enable "2-Step Verification"

2. **Generate App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and generate
   - Copy the 16-character password (no spaces)

3. **Update .env**:
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-16-char-app-password
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   DEFAULT_FROM_EMAIL=your-email@gmail.com
   FRONTEND_URL=http://localhost:3000
   ```

4. **Start Redis** (required for Celery):
   ```powershell
   # Using Docker
   docker run -d -p 6379:6379 redis
   
   # Or local Redis
   redis-server
   ```

5. **Start Celery Worker**:
   ```powershell
   celery -A Ecommerce worker --pool=solo -l info
   ```

6. **Start Django**:
   ```powershell
   python manage.py runserver
   ```

### Alternative Email Providers

**Outlook/Hotmail** (no app password needed):
```env
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_HOST_USER=your-email@outlook.com
EMAIL_HOST_PASSWORD=your-regular-password
EMAIL_PORT=587
```

**SendGrid** (professional, free tier):
```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
EMAIL_PORT=587
```

### Testing Email Verification

1. **Register user**:
   ```
   POST /auth/users/
   {
     "username": "testuser",
     "email": "test@example.com",
     "password": "SecurePass123"
   }
   ```

2. **Check Celery logs** for email send confirmation

3. **Check email inbox** (or console if using console backend)

4. **Click verification link** or call manually:
   ```
   GET /core/verify-email/{token}/
   ```

5. **Verify status**:
   ```
   GET /auth/users/me/
   Authorization: JWT {access_token}
   
   Response: { "email_verified": true }
   ```

6. **Try placing order** (now allowed):
   ```
   POST /store/orders/
   Authorization: JWT {access_token}
   {
     "cart_id": "your-cart-id"
   }
   ```

### Order Protection

Orders are **blocked** until email is verified. Attempting to create an order with unverified email returns:
```json
{
  "error": "Please verify your email address before placing an order."
}
```
Status: `403 Forbidden`

### Token Expiry

- Default expiry: **48 hours**
- Configurable via `VERIFICATION_TOKEN_EXPIRY` in settings
- Expired tokens return error message with instructions to request new verification email

## 📊 Data Population

### Populate Cart Data

A script is provided to generate sample cart and cart item data:

```powershell
python populate_cart_data.py
```

This script will:

- Create 100 cart records with varied timestamps (last 90 days)
- Generate 300-400 cart items (1-8 items per cart)
- Use random products from your database
- Set realistic quantities (1-5 units per item)

**Note**: Ensure you have product data in your database before running this script.

### Seed sample catalog data

```powershell
python manage.py seed_db
```

Executes `store/management/commands/seed.sql` to load baseline collections/products.

### Manual Data Entry

Use the Django Admin interface at `/admin/` to manually add:

- Products
- Collections
- Customers
- Orders
- And more

## 📖 API Documentation

### Example: Creating a Product

**Request:**

```http
POST /store/products/
Content-Type: application/json

{
    "title": "Wireless Mouse",
    "description": "Ergonomic wireless mouse with USB receiver",
    "price": "29.99",
    "inventory": 150,
    "collection": 1
}
```

**Response:**

```json
{
  "id": 1,
  "title": "Wireless Mouse",
  "description": "Ergonomic wireless mouse with USB receiver",
  "price": "29.99",
  "inventory": 150,
  "collection": 1,
  "price_with_tax": "35.99"
}
```

### Example: Retrieving Products

**Request:**

```http
GET /store/products/
```

**Response:**

```json
[
    {
        "id": 1,
        "title": "Wireless Mouse",
        "description": "Ergonomic wireless mouse with USB receiver",
        "price": "29.99",
        "inventory": 150,
        "collection": 1,
        "price_with_tax": "35.99"
    },
    ...
]
```

### Serializer Features

#### Product Serializer

- **Custom Field**: `price_with_tax` - Automatically calculated (20% tax)
- **Validation**: Min value validators for price and inventory
- **Read-only**: `id` and `last_update` fields
- **Query Optimization**: Uses `select_related('collection')` to prevent N+1 queries

#### Collection Serializer

- Simple serialization with `id` and `title`
- Related products accessible via reverse relationship

## 🔒 Business Logic & Validation

### Product Deletion Protection

Products cannot be deleted if they are referenced in any order items:

```python
if OrderItem.objects.filter(product_id=id).count() > 0:
    return Error: "Product cannot be deleted"
```

### Collection Deletion Protection

Collections cannot be deleted if they contain any products:

```python
if Product.objects.filter(collection_id=pk).count() > 0:
    return Error: "Collection cannot be deleted"
```

### Product Image Validation

- Uploads larger than 500 KB are rejected by the validator.
- Files are stored under `media/store/images/`.

### Model Relationships & Cascade Behavior

| Relationship         | on_delete | Behavior                               |
| -------------------- | --------- | -------------------------------------- |
| Product → Collection | PROTECT   | Cannot delete collection with products |
| OrderItem → Product  | PROTECT   | Cannot delete product in orders        |
| CartItem → Product   | CASCADE   | Cart items deleted with product        |
| Order → Customer     | PROTECT   | Cannot delete customer with orders     |
| Address → Customer   | CASCADE   | Address deleted with customer          |

## 🧪 Testing

### Using Django Shell

```powershell
python manage.py shell_plus
```

Example queries:

```python
# Get all products with their collections
products = Product.objects.select_related('collection').all()

# Get products in a specific collection
Collection.objects.get(id=1).product_set.all()

# Get customer orders
Customer.objects.get(id=1).order_set.all()
```

## 📝 Development Notes

### ViewSet Evolution

The project demonstrates the evolution from function-based views to ViewSets:

1. **Function-based views** with `@api_view` decorators
2. **Class-based views** with `APIView`
3. **Generic views** with `ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`
4. **ViewSets** with `ModelViewSet` (current implementation)

### Query Optimization

- Uses `select_related()` for forward ForeignKey relationships
- Prevents N+1 query problems
- Debug Toolbar enabled for query analysis

### Serializer Patterns

- `ModelSerializer` for automatic field generation
- Custom methods for calculated fields
- Proper use of `read_only` for auto-generated fields

## 🤝 Contributing

When contributing to this project:

1. Follow Django and DRF best practices
2. Write descriptive commit messages
3. Update documentation for new features
4. Add tests for new functionality
5. Use `select_related()` or `prefetch_related()` for query optimization

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Developed as a learning project for building RESTful APIs with Django and Django REST Framework.

## 🔮 Future Enhancements

- [ ] Add authentication and authorization (JWT/OAuth)
- [ ] Implement filtering, searching, and pagination
- [ ] Add order processing workflow
- [ ] Integrate payment gateway
- [ ] Add email notifications
- [ ] Implement caching with Redis
- [ ] Add comprehensive test suite
- [ ] API versioning
- [ ] Rate limiting
- [ ] API documentation with Swagger/OpenAPI

---

**Need Help?** Check the Django and DRF documentation:

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
