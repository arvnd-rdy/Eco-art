import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from market.models import Product, ContactMessage
from django.core.files.base import ContentFile
from PIL import Image
import io
import random

class Command(BaseCommand):
    help = 'Seed the database with example users, products, and contact messages.'

    def handle(self, *args, **kwargs):
        # Create users
        users = []
        for i in range(1, 4):
            username = f'user{i}'
            email = f'user{i}@example.com'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password='password123')
                users.append(user)
            else:
                users.append(User.objects.get(username=username))
        self.stdout.write(self.style.SUCCESS('Created example users.'))

        # Create products
        categories = ['eco', 'reuse', 'upcycle', 'other']
        for i in range(1, 7):
            title = f'Product {i}'
            if not Product.objects.filter(title=title).exists():
                description = f'This is a description for {title}.'
                price = round(random.uniform(5, 100), 2)
                category = random.choice(categories)
                location = f'City {i}'
                owner = random.choice(users)
                # Generate a placeholder image
                image = Image.new('RGB', (300, 200), color=(random.randint(100,255), random.randint(100,255), random.randint(100,255)))
                img_io = io.BytesIO()
                image.save(img_io, 'JPEG')
                img_content = ContentFile(img_io.getvalue(), f'product_{i}.jpg')
                product = Product.objects.create(
                    title=title,
                    description=description,
                    price=price,
                    category=category,
                    location=location,
                    owner=owner,
                )
                product.image.save(f'product_{i}.jpg', img_content, save=True)
        self.stdout.write(self.style.SUCCESS('Created example products.'))

        # Create contact messages
        products = list(Product.objects.all())
        for i in range(3):
            sender = users[i % len(users)]
            product = products[i]
            message = f'Hello, I am interested in {product.title}!'
            ContactMessage.objects.create(product=product, sender=sender, message=message)
        self.stdout.write(self.style.SUCCESS('Created example contact messages.'))
        self.stdout.write(self.style.SUCCESS('Seeding complete!')) 