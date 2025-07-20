# EcoArt Market - Sustainable Art Marketplace

A web platform where artists can showcase and sell eco-friendly artwork created with sustainable materials.

## Features

### Core Features
- **User Authentication**: Register, login, logout with secure user management
- **Artwork Listings**: Detailed product pages with comprehensive art information
- **Art Categories**: Specialized categories for different types of eco-art (jewelry, sculptures, wall art, etc.)
- **Art Style Classification**: Abstract, realistic, contemporary, traditional, and more
- **Materials Tracking**: Detailed information about sustainable materials used
- **Sustainability Ratings**: 1-5 scale rating system for eco-friendliness
- **Artist Statements**: Personal stories behind each artwork
- **Dimensions & Specifications**: Detailed artwork measurements and details

### Interactive Features
- **Search & Filter**: Find artwork by category, location, and keywords
- **Contact Artist System**: Direct messaging between buyers and artists
- **Shopping Cart**: Add and manage items in your cart
- **User Visit Tracking**: Analytics for user engagement
- **Responsive Design**: Beautiful Bootstrap 5 UI that works on all devices

### Rating & Review System
- **Product Reviews**: Users can rate and review artwork (1-5 stars)
- **Review Management**: One review per user per product with update capability
- **Average Ratings**: Automatic calculation and display of product ratings
- **Review Count**: Track how many reviews each product has received
- **Star Display**: Visual star ratings on product cards and detail pages
- **Review History**: Users can see their own review history
- **Sample Reviews**: Pre-populated with realistic reviews for demonstration

### Order & Payment System
- **Shopping Cart**: Add items to cart with real-time total calculation
- **Checkout Process**: Complete order flow with shipping and payment information
- **Order Management**: Full order lifecycle with status tracking
- **Payment Methods**: Multiple payment options (Credit Card, PayPal, Bank Transfer, Cash on Delivery)
- **Shipping Information**: Complete address collection and shipping cost calculation
- **Order History**: View all past orders with detailed information
- **Order Tracking**: Real-time order status updates
- **Tax Calculation**: Automatic tax calculation (8% rate)
- **Order Confirmation**: Detailed order confirmation with all information
- **Admin Order Management**: Complete order management in Django admin

### Notification System
- **Real-time Notifications**: Instant notifications for user activities
- **Notification Types**: Reviews, orders, cart actions, system messages, and more
- **Read/Unread Status**: Track notification status with visual indicators
- **Notification Center**: Dedicated page to view and manage all notifications
- **Navigation Badge**: Unread notification count displayed in navigation
- **Mark as Read**: Individual and bulk mark-as-read functionality
- **Related Links**: Direct links to related products, orders, and users
- **Time Stamps**: Relative time display (e.g., "2 hours ago")
- **Admin Management**: Complete notification management in Django admin
- **Sample Notifications**: Pre-populated with realistic notifications for testing

### Artist Features
- **Artist Profiles**: Detailed profiles with bio, location, and social links
- **Portfolio Management**: Artists can showcase their entire collection
- **Product Upload**: Easy-to-use form for adding new artwork
- **Sales Analytics**: Track product performance and engagement

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. (Optional) Populate with sample data:
```bash
python manage.py create_eco_artists
python manage.py populate_eco_art
python manage.py add_sample_reviews
python manage.py add_sample_notifications
```

6. Run the development server:
```bash
python manage.py runserver
```

## Tech Stack

- **Backend**: Django 4.x with class-based views
- **Frontend**: Django Templates + Bootstrap 5
- **Database**: SQLite (easily configurable for production)
- **Authentication**: Django's built-in auth system
- **File Storage**: Django's MEDIA_ROOT for artwork images
- **Forms**: Django Forms with custom validation
- **Admin Interface**: Customized Django admin for easy management

## Project Structure

```
Django_final_project/
├── market/                 # Main app
│   ├── models.py          # Product, Review, Order, OrderItem, Profile, ContactMessage, Notification models
│   ├── views.py           # Class-based views for all functionality
│   ├── forms.py           # Forms for products, reviews, orders, profiles
│   ├── admin.py           # Customized admin interface
│   ├── urls.py            # URL routing
│   └── templates/         # HTML templates
├── greenmarket/           # Project settings
├── media/                 # Uploaded images
├── static/                # Static files
└── manage.py             # Django management script
```

## Key Models

- **Product**: Artwork with categories, styles, materials, sustainability ratings
- **Review**: User ratings and comments for products
- **Order**: Complete order information with shipping and payment details
- **OrderItem**: Individual items within orders with pricing
- **Notification**: User notifications for various activities and system events
- **Profile**: Extended user profiles with artist information
- **ContactMessage**: Communication between buyers and artists

## Order Flow

1. **Browse Products**: Users browse the marketplace and add items to cart
2. **Cart Management**: View cart with totals, shipping costs, and tax calculation
3. **Checkout**: Complete shipping information and select payment method
4. **Order Confirmation**: Receive order confirmation with order number
5. **Order Tracking**: View order history and track order status
6. **Admin Management**: Admins can manage orders, update status, and process payments

## Notification Types

- **Welcome**: New user welcome messages
- **Review Received**: When someone reviews your artwork
- **Order Placed**: When orders are placed (buyer and seller notifications)
- **Order Status Changed**: Order status updates
- **Product Added/Removed from Cart**: Cart activity notifications
- **Product Uploaded**: Confirmation when artwork is uploaded
- **System**: General system notifications
- **Product Liked**: When someone likes your artwork (future feature)
- **New Follower**: When someone follows your profile (future feature)
- **Product Shared**: When someone shares your artwork (future feature)

## Payment Features

- **Multiple Payment Methods**: Credit Card, PayPal, Bank Transfer, Cash on Delivery
- **Payment Status Tracking**: Pending, Paid, Failed, Refunded
- **Order Status Management**: Pending, Processing, Shipped, Delivered, Cancelled
- **Automatic Calculations**: Subtotal, shipping, tax, and total calculations
- **Order Number Generation**: Unique order numbers for tracking

## Future Enhancements

- Payment gateway integration (Stripe, PayPal)
- Advanced search filters
- Wishlist functionality
- Order management system
- Artist verification badges
- Commission request system
- Artwork licensing options
- Email notifications for order updates
- Shipping tracking integration
- Return and refund management
- Push notifications for mobile
- Notification preferences and settings
- Real-time chat system
- Social media integration 