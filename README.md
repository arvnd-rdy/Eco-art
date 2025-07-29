# EcoArt Market - Sustainable Art Marketplace

A web platform where artists can showcase and sell eco-friendly artwork created with sustainable materials.

## Features

### Core Features
- **Advanced User Authentication**: Complete authentication system with enhanced security
  - ✅ **Secure Login/Logout**: Custom login view with proper error handling
  - ✅ **User Registration**: Signup with email verification
  - ✅ **Password Reset**: Real email sending with Gmail SMTP integration
  - ✅ **Change Password**: In-profile password change functionality
  - ✅ **Email Validation**: Checks if user exists before sending reset emails
  - ✅ **Session Management**: Prevents logout after password changes
  - ✅ **Error Handling**: Clear error messages for invalid credentials
- **Artwork Listings**: Detailed product pages with comprehensive art information
- **Art Categories**: Specialized categories for different types of eco-art (jewelry, sculptures, wall art, etc.)
- **Art Style Classification**: Abstract, realistic, contemporary, traditional, and more
- **Materials Tracking**: Detailed information about sustainable materials used
- **Sustainability Ratings**: 1-5 scale rating system for eco-friendliness
- **Artist Statements**: Personal stories behind each artwork
- **Dimensions & Specifications**: Detailed artwork measurements and details

### Data Management & Fixtures
- **Pre-loaded Sample Data**: Comprehensive fixtures for consistent demos
  - ✅ **User Fixtures**: 14 sample users with different roles (artists, buyers, admin)
  - ✅ **Product Fixtures**: 50+ eco-friendly artwork samples
  - ✅ **Review Fixtures**: Realistic reviews and ratings
  - ✅ **Profile Fixtures**: Complete artist profiles with bios and locations
  - ✅ **Quick Setup**: `python manage.py loaddata fixtures/*.json`
  - ✅ **Consistent Testing**: Same data across all team members
  - ✅ **Demo Ready**: Instantly populated with meaningful data

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

5. Load sample data (Fixtures):
```bash
python manage.py loaddata fixtures/users.json
python manage.py loaddata fixtures/profiles.json
python manage.py loaddata fixtures/products.json
python manage.py loaddata fixtures/reviews.json
```

6. (Optional) Create additional sample data:
```bash
python manage.py create_eco_artists
python manage.py populate_eco_art
python manage.py add_sample_reviews
python manage.py add_sample_notifications
```

7. Run the development server:
```bash
python manage.py runserver
```

## Authentication Features

### Login System
- **Custom Login View**: Enhanced error handling and user feedback
- **Error Messages**: Clear validation for invalid credentials
- **Success Messages**: Welcome back notifications
- **Form Validation**: Proper field validation and error display

### Password Management
- **Password Reset**: Real email sending with Gmail SMTP
- **Email Validation**: Checks user existence before sending emails
- **Secure Tokens**: Django's built-in secure token system
- **Change Password**: In-profile password change functionality
- **Session Preservation**: Maintains login after password changes

### User Profiles
- **Extended Profiles**: Bio, location, phone, social links
- **Profile Management**: Edit profile information
- **Role-based Features**: Different views for buyers/sellers
- **Profile Pictures**: Upload and manage profile images

## Email Configuration

The project uses Gmail SMTP for sending password reset emails:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

**Setup Instructions:**
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password for Django
3. Update the email settings in `greenmarket/settings.py`

## Tech Stack

- **Backend**: Django 4.x with class-based views
- **Frontend**: Django Templates + Bootstrap 5
- **Database**: SQLite (easily configurable for production)
- **Authentication**: Custom Django auth system with enhanced features
- **Email**: Gmail SMTP for password reset functionality
- **File Storage**: Django's MEDIA_ROOT for artwork images
- **Forms**: Django Forms with custom validation
- **Admin Interface**: Customized Django admin for easy management

## Project Structure

```
Eco-art/
├── market/                 # Main app
│   ├── models.py          # Product, Review, Order, OrderItem, Profile, ContactMessage, Notification models
│   ├── views.py           # Class-based views including custom auth views
│   ├── forms.py           # Forms for products, reviews, orders, profiles
│   ├── admin.py           # Customized admin interface
│   ├── urls.py            # URL routing with custom auth URLs
│   └── templates/         # HTML templates
├── greenmarket/           # Project settings
├── fixtures/              # Sample data fixtures
│   ├── users.json         # Sample users
│   ├── profiles.json      # User profiles
│   ├── products.json      # Sample products
│   └── reviews.json       # Sample reviews
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
- **User**: Django's built-in user model with custom authentication

## Authentication Flow

1. **Registration**: Users sign up with username, email, and password
2. **Login**: Secure login with error handling and validation
3. **Password Reset**: Email-based password reset with validation
4. **Profile Management**: Edit profile information and change password
5. **Logout**: Secure logout with session cleanup

## Fixtures & Sample Data

The project includes comprehensive fixtures for easy setup and consistent demos:

- **14 Sample Users**: Including admin, artists, and buyers
- **50+ Products**: Eco-friendly artwork samples
- **Realistic Reviews**: Pre-populated reviews and ratings
- **Complete Profiles**: Artist profiles with bios and locations

**Quick Setup:**
```bash
python manage.py loaddata fixtures/*.json
```

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
- Two-factor authentication
- Email verification for new accounts
- Password strength requirements
- Account lockout after failed attempts 