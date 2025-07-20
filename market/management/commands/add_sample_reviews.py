from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from market.models import Product, Review
import random

class Command(BaseCommand):
    help = 'Add sample reviews to products'

    def handle(self, *args, **options):
        # Sample review comments
        review_comments = [
            "Absolutely stunning piece! The craftsmanship is incredible and the sustainable materials make it even more special.",
            "Love the eco-friendly approach. This artwork not only looks beautiful but also helps the environment.",
            "The artist's vision really shines through. A perfect blend of creativity and sustainability.",
            "Amazing attention to detail. You can tell this was made with care and environmental consciousness.",
            "This piece adds such warmth to my space. The sustainable materials give it a unique character.",
            "Incredible work! The recycled materials create such interesting textures and patterns.",
            "The artist's statement really resonates with me. This piece tells such an important story.",
            "Beautiful craftsmanship and eco-friendly materials. Exactly what I was looking for!",
            "This artwork exceeded my expectations. The sustainable approach makes it even more meaningful.",
            "Stunning piece that perfectly balances aesthetics with environmental responsibility.",
            "The materials used are so unique and the story behind it is inspiring.",
            "Love how this piece combines traditional techniques with modern sustainable practices.",
            "The attention to detail is remarkable. A true work of art that respects our planet.",
            "This piece has become the focal point of my room. The sustainable materials give it such character.",
            "Incredible talent! The way recycled materials are transformed into beauty is inspiring.",
            "The artist's commitment to sustainability really shows in the quality of this piece.",
            "A beautiful reminder that art can be both stunning and environmentally conscious.",
            "The craftsmanship is outstanding and the eco-friendly materials make it even better.",
            "This piece has such a unique story to tell. Love the sustainable approach!",
            "Absolutely gorgeous! The sustainable materials add such depth and meaning to the artwork."
        ]

        # Get all products and users
        products = Product.objects.all()
        users = User.objects.all()

        if not products.exists():
            self.stdout.write(
                self.style.ERROR('No products found. Please create some products first.')
            )
            return

        if not users.exists():
            self.stdout.write(
                self.style.ERROR('No users found. Please create some users first.')
            )
            return

        created_count = 0

        for product in products:
            # Skip if product owner has no reviews (they shouldn't review their own work)
            other_users = [user for user in users if user != product.owner]
            
            if not other_users:
                continue

            # Add 2-5 reviews per product
            num_reviews = random.randint(2, 5)
            selected_users = random.sample(other_users, min(num_reviews, len(other_users)))

            for user in selected_users:
                # Check if user already reviewed this product
                if not Review.objects.filter(product=product, user=user).exists():
                    rating = random.randint(4, 5)  # Mostly positive reviews
                    comment = random.choice(review_comments)
                    
                    Review.objects.create(
                        product=product,
                        user=user,
                        rating=rating,
                        comment=comment
                    )
                    
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Added review by {user.username} for {product.title}')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Successfully created {created_count} sample reviews!')
        )
        self.stdout.write(
            self.style.SUCCESS('✨ Products now have ratings and reviews to showcase the feature!')
        ) 