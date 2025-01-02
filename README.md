# Pharmacy Management System

A full-stack pharmacy management system with a Django backend and Flutter frontend.

## Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Apply database migrations:
```bash
python manage.py migrate
```

3. Create a superuser:
```bash
python manage.py createsuperuser
```

4. Run the development server:
```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000/api/`.

## API Endpoints

### Authentication
- `POST /api/token/` - Get JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Products
- `GET /api/products/` - List all products
- `GET /api/products/{id}/` - Get product details

### Cart
- `GET /api/cart/` - List cart items
- `POST /api/cart/add/` - Add item to cart
- `PUT /api/cart/{id}/` - Update cart item
- `DELETE /api/cart/{id}/` - Remove cart item

### Addresses
- `GET /api/address/` - List addresses
- `POST /api/address/` - Add new address
- `PUT /api/address/{id}/` - Update address
- `PATCH /api/address/{id}/` - Partially update address
- `DELETE /api/address/{id}/` - Delete address

### Orders
- `GET /api/orders/` - List orders
- `POST /api/orders/` - Create order
- `GET /api/orders/{id}/` - Get order details

## Flutter App Setup

1. Install dependencies:
```bash
flutter pub get
```

2. Update API configuration:
- For Android Emulator: `http://10.0.2.2:8000/api`
- For iOS Simulator: `http://localhost:8000/api`
- For Physical Device: Use your machine's IP address

3. Run the app:
```bash
flutter run
```

## Features

- User authentication with JWT
- Product browsing and searching
- Shopping cart management
- Address management
- Order placement and tracking
- Prescription upload and management

## Dependencies

### Backend
- Django 5.1.2
- Django REST Framework 3.15.2
- Simple JWT 5.3.1
- CORS Headers 4.5.0
- Pillow 11.0.0
- Python Dotenv 1.0.0
- DRF YASG 1.21.7
- Django Filter 23.5

### Frontend
- Flutter (latest stable)
- HTTP package
- Provider for state management
- Flutter Secure Storage for token storage
- Image Picker for prescription uploads
