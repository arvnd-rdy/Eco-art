from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

# Create your models here.

# Additional models to meet 5-member team requirements (10 models total)

class Category(models.Model):
    """Art category model for better organization"""
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['display_name']
    
    def __str__(self):
        return self.display_name

class ArtStyle(models.Model):
    """Art style model for better categorization"""
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_name']
    
    def __str__(self):
        return self.display_name

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('eco_jewelry', '🌿 Eco Jewelry'),
        ('recycled_sculptures', '🔩 Recycled Metal Sculptures'),
        ('wall_art', '🎨 Wall Art & Fine Art'),
        ('home_decor', '🏠 Home Decor & Sculptures'),
        ('handmade_artisan', '🔨 Handmade & Artisan Products'),
        ('natural_sustainable', '🌱 Natural & Sustainable Products'),
        ('sustainable_fashion', '👕 Sustainable Fashion'),
        ('showcase_educational', '📸 Showcase & Educational'),
        ('other', '✨ Other'),
    ]
    
    ART_STYLE_CHOICES = [
        ('abstract', 'Abstract'),
        ('realistic', 'Realistic'),
        ('contemporary', 'Contemporary'),
        ('traditional', 'Traditional'),
        ('modern', 'Modern'),
        ('folk', 'Folk Art'),
        ('minimalist', 'Minimalist'),
        ('steampunk', 'Steampunk'),
        ('collage', 'Collage'),
        ('sculptural', 'Sculptural'),
        ('wearable', 'Wearable Art'),
        ('functional', 'Functional Art'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    art_style = models.CharField(max_length=20, choices=ART_STYLE_CHOICES, blank=True, null=True)
    materials = models.TextField(help_text="List the eco-friendly materials used", blank=True, null=True)
    dimensions = models.CharField(max_length=50, help_text="e.g., 24\" x 36\" or 60cm x 90cm", blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    location = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    artist_statement = models.TextField(help_text="Tell the story behind your artwork", blank=True, null=True)
    sustainability_rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)], 
        help_text="How eco-friendly is this piece? (1-5)",
        default=3
    )

    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    
    @property
    def review_count(self):
        """Get total number of reviews"""
        return self.reviews.count()

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'product']  # One wishlist entry per user per product
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user.username} wishlisted {self.product.title}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('review_received', 'Review Received'),
        ('order_placed', 'Order Placed'),
        ('order_status_changed', 'Order Status Changed'),
        ('product_added_to_cart', 'Product Added to Cart'),
        ('product_removed_from_cart', 'Product Removed from Cart'),
        ('product_added_to_wishlist', 'Product Added to Wishlist'),
        ('product_removed_from_wishlist', 'Product Removed from Wishlist'),
        ('new_follower', 'New Follower'),
        ('product_liked', 'Product Liked'),
        ('product_shared', 'Product Shared'),
        ('welcome', 'Welcome'),
        ('system', 'System'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    related_product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    related_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_notifications')
    related_order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type} for {self.user.username}"
    
    @property
    def icon_class(self):
        """Return appropriate FontAwesome icon class based on notification type"""
        icon_map = {
            'review_received': 'fas fa-star',
            'order_placed': 'fas fa-shopping-bag',
            'order_status_changed': 'fas fa-truck',
            'product_added_to_cart': 'fas fa-cart-plus',
            'product_removed_from_cart': 'fas fa-cart-minus',
            'product_added_to_wishlist': 'fas fa-heart',
            'product_removed_from_wishlist': 'fas fa-heart-broken',
            'new_follower': 'fas fa-user-plus',
            'product_liked': 'fas fa-heart',
            'product_shared': 'fas fa-share',
            'welcome': 'fas fa-hand-wave',
            'system': 'fas fa-bell',
        }
        return icon_map.get(self.notification_type, 'fas fa-bell')
    
    @property
    def color_class(self):
        """Return appropriate Bootstrap color class based on notification type"""
        color_map = {
            'review_received': 'text-warning',
            'order_placed': 'text-success',
            'order_status_changed': 'text-info',
            'product_added_to_cart': 'text-primary',
            'product_removed_from_cart': 'text-secondary',
            'product_added_to_wishlist': 'text-danger',
            'product_removed_from_wishlist': 'text-secondary',
            'new_follower': 'text-success',
            'product_liked': 'text-danger',
            'product_shared': 'text-info',
            'welcome': 'text-success',
            'system': 'text-primary',
        }
        return color_map.get(self.notification_type, 'text-primary')

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    comment = models.TextField(help_text="Share your thoughts about this artwork")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['product', 'user']  # One review per user per product
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}'s review of {self.product.title}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash_on_delivery', 'Cash on Delivery'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    
    # Shipping Information
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_zip_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=20)
    
    # Order Totals
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate unique order number
            import random
            import string
            while True:
                order_num = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                if not Order.objects.filter(order_number=order_num).exists():
                    self.order_number = order_num
                    break
        super().save(*args, **kwargs)
    
    @property
    def item_count(self):
        """Get total number of items in order"""
        return sum(item.quantity for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order
    
    def __str__(self):
        return f"{self.quantity}x {self.product.title} in Order {self.order.order_number}"
    
    @property
    def total_price(self):
        return self.price * self.quantity

class ContactMessage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} about {self.product.title}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    social_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
