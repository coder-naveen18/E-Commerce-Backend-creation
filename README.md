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
- [Data Population](#data-population)
- [API Documentation](#api-documentation)

## ✨ Features

- **Product Management**: Full CRUD operations for products with pricing, inventory, and descriptions
- **Collection Management**: Organize products into collections with featured products
- **Customer Management**: Track customer information with membership tiers (Gold, Silver, Bronze)
- **Order Management**: Process orders with payment status tracking
- **Shopping Cart**: Cart and cart item management for customer shopping sessions
- **Promotion System**: Apply promotions and discounts to products
- **Address Management**: One-to-one relationship for customer addresses
- **Phone Number Support**: International phone number validation using phonenumber_field
- **Optimized Queries**: Uses `select_related()` to prevent N+1 query problems
- **Data Validation**: Comprehensive validation using Django REST Framework serializers
- **Protection Rules**: Prevents deletion of products/collections associated with orders

## 🛠 Tech Stack

- **Framework**: Django 6.0+
- **API**: Django REST Framework
- **Database**: MySQL (development) - easily configurable for PostgreSQL/In-build django Sqlite
- **Utilities**:
  - `django-extensions` - Additional management commands
  - `django-debug-toolbar` - Performance debugging
  - `phonenumber_field` - International phone number validation
  - `python-dotenv` - Environment variable management

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
│   └── migrations/         # Database migrations
│
├── likes/                  # Likes functionality app
├── tags/                   # Tags functionality app
├── playground/             # Testing/experimental app
├── store_custom/           # Custom store extensions
│
├── manage.py               # Django management script
├── db.sqlite3              # SQLite database
├── populate_cart_data.py   # Script to populate cart data
└── .env                    # Environment variables (not in repo)
```

## 🗄 Database Models

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

### Collection

Product categorization with optional featured product.

```python
- title: CharField(max_length=255)
- featured_product: ForeignKey to Product (nullable)
```

### Customer

Customer information with membership tiers.

```python
- first_name: CharField(max_length=255)
- last_name: CharField(max_length=255)
- email: EmailField (unique)
- phone: PhoneNumberField (optional)
- birth_date: DateField
- membership: CharField (Gold/Silver/Bronze)
```

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
- created_at: DateTimeField (auto_now_add)

CartItem:
- cart: ForeignKey to Cart (CASCADE)
- product: ForeignKey to Product (CASCADE)
- quantity: PositiveSmallIntegerField
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
   pip install django djangorestframework django-extensions django-debug-toolbar phonenumber-field python-dotenv
   ```

4. **Create `.env` file**

   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
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

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

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
