from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from market.models import Product, Wishlist
import random

class Command(BaseCommand):
    help = 'Add sample wishlist data for testing'

    def handle(self, *args, **options):
        users = User.objects.all()
        products = Product.objects.all()
        
        if not users.exists():
            self.stdout.write(self.style.ERROR('No users found. Please create users first.'))
            return
            
        if not products.exists():
            self.stdout.write(self.style.ERROR('No products found. Please create products first.'))
            return
        
        # Clear existing wishlist data
        Wishlist.objects.all().delete()
        
        wishlist_count = 0
        
        # Add random wishlist items for each user
        for user in users:
            # Skip if user has no products (they might be sellers only)
            if user.products.exists():
                # Add 2-5 random products to wishlist for each user
                num_wishlist_items = random.randint(2, 5)
                available_products = [p for p in products if p.owner != user]  # Don't wishlist own products
                
                if available_products:
                    selected_products = random.sample(available_products, min(num_wishlist_items, len(available_products)))
                    
                    for product in selected_products:
                        Wishlist.objects.create(user=user, product=product)
                        wishlist_count += 1
                        
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Added "{product.title}" to {user.username}\'s wishlist'
                            )
                        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {wishlist_count} wishlist items for {users.count()} users'
            )
        ) 