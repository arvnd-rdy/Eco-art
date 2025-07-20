from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from market.models import Product, Notification
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Add sample notifications for testing'

    def handle(self, *args, **options):
        users = User.objects.all()
        products = Product.objects.all()
        
        if not users.exists():
            self.stdout.write(self.style.ERROR('No users found. Please create users first.'))
            return
        
        if not products.exists():
            self.stdout.write(self.style.ERROR('No products found. Please create products first.'))
            return
        
        # Sample notification data
        sample_notifications = [
            {
                'type': 'welcome',
                'title': 'Welcome to EcoArt Market!',
                'message': 'Thank you for joining our community of eco-conscious artists and art lovers. Start exploring sustainable artwork today!'
            },
            {
                'type': 'review_received',
                'title': 'New Review Received!',
                'message': 'Sarah left a 5-star review for your artwork "Recycled Metal Sculpture"'
            },
            {
                'type': 'order_placed',
                'title': 'New Order for Your Artwork!',
                'message': 'John purchased "Eco Jewelry Necklace" in order #ABC12345'
            },
            {
                'type': 'product_added_to_cart',
                'title': 'Added to Cart',
                'message': '"Sustainable Wall Art" has been added to your cart'
            },
            {
                'type': 'system',
                'title': 'Product Uploaded Successfully!',
                'message': 'Your artwork "Handmade Ceramic Vase" has been uploaded and is now live on the marketplace.'
            },
            {
                'type': 'order_status_changed',
                'title': 'Order Status Updated',
                'message': 'Your order #XYZ67890 has been shipped and is on its way!'
            },
            {
                'type': 'product_liked',
                'title': 'Product Liked',
                'message': 'Emma liked your artwork "Natural Dye Scarf"'
            },
            {
                'type': 'new_follower',
                'title': 'New Follower',
                'message': 'Michael started following your artist profile'
            }
        ]
        
        notifications_created = 0
        
        for user in users:
            # Create 3-8 random notifications for each user
            num_notifications = random.randint(3, 8)
            
            for i in range(num_notifications):
                notification_data = random.choice(sample_notifications)
                
                # Create notification with random timing (within last 7 days)
                created_at = timezone.now() - timedelta(
                    days=random.randint(0, 7),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                
                notification = Notification.objects.create(
                    user=user,
                    notification_type=notification_data['type'],
                    title=notification_data['title'],
                    message=notification_data['message'],
                    related_product=random.choice(products) if random.choice([True, False]) else None,
                    related_user=random.choice(users) if random.choice([True, False]) else None,
                    is_read=random.choice([True, False]),
                    created_at=created_at
                )
                
                notifications_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {notifications_created} sample notifications for {users.count()} users'
            )
        ) 