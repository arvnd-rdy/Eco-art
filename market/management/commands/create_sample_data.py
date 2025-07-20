import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from market.models import Product, Profile
from django.core.files.base import ContentFile
from PIL import Image
import io
import random

class Command(BaseCommand):
    help = 'Create 10 users with 4 products each for GreenMarket'

    def handle(self, *args, **kwargs):
        # Sample eco-friendly product data
        eco_products = [
            {
                'title': 'Bamboo Water Bottle',
                'description': 'Sustainable bamboo water bottle, perfect for reducing plastic waste. Made from 100% natural bamboo.',
                'category': 'eco',
                'price_range': (15.00, 25.00)
            },
            {
                'title': 'Reusable Shopping Bags',
                'description': 'Set of 3 cotton shopping bags. Durable, washable, and perfect for grocery shopping.',
                'category': 'reuse',
                'price_range': (12.00, 20.00)
            },
            {
                'title': 'Solar-Powered Garden Lights',
                'description': 'Beautiful solar-powered LED garden lights. Charge during the day, light up your garden at night.',
                'category': 'eco',
                'price_range': (25.00, 40.00)
            },
            {
                'title': 'Upcycled Denim Tote',
                'description': 'Handmade tote bag made from recycled denim jeans. Unique and environmentally friendly.',
                'category': 'upcycle',
                'price_range': (18.00, 30.00)
            },
            {
                'title': 'Beeswax Food Wraps',
                'description': 'Natural beeswax food wraps to replace plastic wrap. Reusable and biodegradable.',
                'category': 'eco',
                'price_range': (8.00, 15.00)
            },
            {
                'title': 'Recycled Paper Notebook',
                'description': 'Notebook made from 100% recycled paper. Perfect for eco-conscious students and professionals.',
                'category': 'reuse',
                'price_range': (5.00, 12.00)
            },
            {
                'title': 'Upcycled Glass Vase',
                'description': 'Beautiful vase made from recycled glass bottles. Each piece is unique and handcrafted.',
                'category': 'upcycle',
                'price_range': (20.00, 35.00)
            },
            {
                'title': 'Organic Cotton T-Shirt',
                'description': 'Comfortable t-shirt made from organic cotton. No harmful chemicals, better for you and the planet.',
                'category': 'eco',
                'price_range': (22.00, 35.00)
            },
            {
                'title': 'Reusable Coffee Cup',
                'description': 'Insulated reusable coffee cup made from stainless steel. Keep your drinks hot or cold for hours.',
                'category': 'reuse',
                'price_range': (15.00, 25.00)
            },
            {
                'title': 'Upcycled Wood Shelf',
                'description': 'Rustic shelf made from reclaimed wood. Perfect for displaying plants or books.',
                'category': 'upcycle',
                'price_range': (45.00, 70.00)
            },
            {
                'title': 'Bamboo Toothbrush Set',
                'description': 'Set of 4 biodegradable bamboo toothbrushes. Eco-friendly alternative to plastic toothbrushes.',
                'category': 'eco',
                'price_range': (8.00, 15.00)
            },
            {
                'title': 'Recycled Plastic Plant Pots',
                'description': 'Plant pots made from 100% recycled plastic. Perfect for your indoor garden.',
                'category': 'reuse',
                'price_range': (6.00, 12.00)
            },
            {
                'title': 'Upcycled Tire Planter',
                'description': 'Creative planter made from upcycled car tires. Great for outdoor gardening.',
                'category': 'upcycle',
                'price_range': (30.00, 50.00)
            },
            {
                'title': 'Solar Phone Charger',
                'description': 'Portable solar charger for your phone. Harness the power of the sun to charge your devices.',
                'category': 'eco',
                'price_range': (35.00, 55.00)
            },
            {
                'title': 'Reusable Food Containers',
                'description': 'Set of 5 glass food containers with bamboo lids. Perfect for meal prep and storage.',
                'category': 'reuse',
                'price_range': (25.00, 40.00)
            }
        ]

        locations = [
            'Toronto, ON', 'Vancouver, BC', 'Montreal, QC', 'Calgary, AB', 
            'Edmonton, AB', 'Ottawa, ON', 'Winnipeg, MB', 'Quebec City, QC',
            'Hamilton, ON', 'Kitchener, ON', 'London, ON', 'Victoria, BC'
        ]

        # Create 10 users (user1 to user10)
        users = []
        for i in range(1, 11):
            username = f'user{i}'
            email = f'user{i}@greenmarket.com'
            
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username, 
                    email=email, 
                    password='password123',
                    first_name=f'User{i}',
                    last_name='Green'
                )
                
                # Create profile for the user
                profile, created = Profile.objects.get_or_create(
                    user=user,
                    defaults={
                        'bio': f'I am user{i}, passionate about eco-friendly products and sustainable living.',
                        'location': random.choice(locations),
                        'phone': f'555-{1000 + i:04d}',
                        'social_link': f'https://instagram.com/user{i}'
                    }
                )
                
                users.append(user)
                self.stdout.write(f'Created user: {username}')
            else:
                user = User.objects.get(username=username)
                # Ensure user has a profile
                profile, created = Profile.objects.get_or_create(
                    user=user,
                    defaults={
                        'bio': f'I am user{i}, passionate about eco-friendly products and sustainable living.',
                        'location': random.choice(locations),
                        'phone': f'555-{1000 + i:04d}',
                        'social_link': f'https://instagram.com/user{i}'
                    }
                )
                users.append(user)
                self.stdout.write(f'User {username} already exists, ensured profile exists')

        # Create 4 products for each user
        for user in users:
            user_products = random.sample(eco_products, 4)  # Select 4 random products for each user
            
            for product_data in user_products:
                # Generate a unique title by adding user prefix
                title = f"{user.username.capitalize()}'s {product_data['title']}"
                
                if not Product.objects.filter(title=title).exists():
                    # Generate random price within the range
                    min_price, max_price = product_data['price_range']
                    price = round(random.uniform(min_price, max_price), 2)
                    
                    # Generate a placeholder image with user-specific colors
                    color1 = random.randint(100, 255)
                    color2 = random.randint(100, 255)
                    color3 = random.randint(100, 255)
                    image = Image.new('RGB', (400, 300), color=(color1, color2, color3))
                    
                    # Add some text to the image
                    from PIL import ImageDraw, ImageFont
                    draw = ImageDraw.Draw(image)
                    try:
                        font = ImageFont.truetype("arial.ttf", 20)
                    except:
                        font = ImageFont.load_default()
                    
                    draw.text((50, 150), f"{user.username}'s Product", fill=(255, 255, 255), font=font)
                    
                    img_io = io.BytesIO()
                    image.save(img_io, 'JPEG')
                    img_content = ContentFile(img_io.getvalue(), f'{user.username}_product.jpg')
                    
                    # Get user's profile location
                    profile = Profile.objects.get(user=user)
                    
                    product = Product.objects.create(
                        title=title,
                        description=product_data['description'],
                        price=price,
                        category=product_data['category'],
                        location=profile.location,
                        owner=user,
                    )
                    product.image.save(f'{user.username}_product.jpg', img_content, save=True)
                    
                    self.stdout.write(f'Created product: {title} for {user.username}')
                else:
                    self.stdout.write(f'Product {title} already exists')

        self.stdout.write(self.style.SUCCESS('Successfully created 10 users with 4 products each!'))
        self.stdout.write('All users have password: password123') 