from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from market.models import Product, Profile
from decimal import Decimal
import os
import random

class Command(BaseCommand):
    help = 'Populate the database with eco-art products assigned to specific artists'

    def add_arguments(self, parser):
        parser.add_argument(
            '--images-dir',
            type=str,
            default='media/prodcuts',  # Note: using the actual folder name with typo
            help='Directory containing the eco-art images'
        )

    def handle(self, *args, **options):
        # Get the 10 artists we created
        artists = User.objects.filter(
            username__in=[
                'sarah_greenwood', 'maria_rodriguez', 'david_chen', 'emma_thompson',
                'alex_rivera', 'lisa_park', 'marcus_johnson', 'sophie_williams',
                'carlos_mendez', 'aisha_patel'
            ]
        )
        
        if artists.count() != 10:
            self.stdout.write(
                self.style.ERROR('Please run create_eco_artists command first!')
            )
            return

        # Define artist-product assignments based on specialties
        artist_assignments = {
            'sarah_greenwood': {
                'categories': ['recycled_sculptures'],
                'image_patterns': ['recycled-metal', 'steampunk', 'recycled-spark', 'recycled-objects'],
                'art_styles': ['steampunk', 'sculptural'],
                'price_range': (150, 800),
                'materials': [
                    'Recycled automotive parts, scrap metal, brass fittings',
                    'Recycled metal scraps, copper wire, steel base',
                    'Found objects, recycled materials, sustainable adhesives',
                    'Recycled spark plugs, scrap metal, industrial materials'
                ]
            },
            'maria_rodriguez': {
                'categories': ['eco_jewelry'],
                'image_patterns': ['jewelry', 'eco-friendly-jewelry', 'cled', 'reclaimed-wood-jewelry'],
                'art_styles': ['wearable'],
                'price_range': (25, 150),
                'materials': [
                    'Recycled silver, sustainable bamboo, natural hemp cord',
                    'Reclaimed wood, natural leather, brass hardware',
                    'Recycled metals, natural stones, eco-friendly finishes',
                    'Sustainable bamboo, organic cotton, natural dyes'
                ]
            },
            'david_chen': {
                'categories': ['wall_art'],
                'image_patterns': ['eco-wall-art', 'sustainable-fine-art', 'three-waves-collage', 'universal-vulnerability'],
                'art_styles': ['contemporary', 'abstract', 'collage'],
                'price_range': (200, 600),
                'materials': [
                    'Recycled paper, natural dyes, sustainable glue, reclaimed wood frame',
                    'Eco-friendly acrylic paints, organic cotton canvas, reclaimed wood frame',
                    'Mixed media, recycled materials, sustainable adhesives',
                    'Natural pigments, sustainable canvas, eco-friendly varnish'
                ]
            },
            'emma_thompson': {
                'categories': ['sustainable_fashion'],
                'image_patterns': ['sustainable-clothing'],
                'art_styles': ['wearable'],
                'price_range': (80, 300),
                'materials': [
                    '100% organic cotton, natural dyes, sustainable buttons',
                    'Recycled fabrics, natural fibers, eco-friendly thread',
                    'Sustainable textiles, natural dyes, ethical production',
                    'Organic materials, natural finishes, sustainable hardware'
                ]
            },
            'alex_rivera': {
                'categories': ['natural_sustainable'],
                'image_patterns': ['natural-eco-paints'],
                'art_styles': ['functional'],
                'price_range': (30, 150),
                'materials': [
                    'Natural earth pigments, plant-based binders, recycled packaging',
                    'Organic materials, natural dyes, sustainable processes',
                    'Upcycled materials, natural finishes, eco-friendly adhesives',
                    'Zero-waste materials, natural fibers, sustainable practices'
                ]
            },
            'lisa_park': {
                'categories': ['home_decor'],
                'image_patterns': ['eco-home-decor', 'handmade-clay'],
                'art_styles': ['functional', 'sculptural'],
                'price_range': (50, 300),
                'materials': [
                    'Natural clay, eco-friendly glazes, sustainable firing process',
                    'Reclaimed wood, natural finishes, sustainable hardware',
                    'Recycled materials, natural fibers, eco-friendly adhesives',
                    'Sustainable ceramics, natural glazes, organic materials'
                ]
            },
            'marcus_johnson': {
                'categories': ['handmade_artisan'],
                'image_patterns': ['reclaimed-wood', 'handmade-eco-product'],
                'art_styles': ['functional', 'sculptural'],
                'price_range': (100, 400),
                'materials': [
                    'Reclaimed wood, natural finishes, sustainable hardware',
                    'Salvaged timber, eco-friendly adhesives, natural oils',
                    'Recycled wood, sustainable joinery, natural stains',
                    'Upcycled lumber, traditional techniques, eco-friendly finishes'
                ]
            },
            'sophie_williams': {
                'categories': ['recycled_sculptures', 'wall_art'],
                'image_patterns': ['recycled-metal', 'fine-art', 'collage', 'vulnerability'],
                'art_styles': ['contemporary', 'sculptural', 'mixed_media'],
                'price_range': (200, 800),
                'materials': [
                    'Recycled metal components, sustainable welding, natural patina',
                    'Mixed media, recycled materials, sustainable adhesives',
                    'Found objects, metal scraps, eco-friendly finishes',
                    'Salvaged materials, sustainable techniques, natural elements'
                ]
            },
            'carlos_mendez': {
                'categories': ['handmade_artisan'],
                'image_patterns': ['artisan-handmade', 'handmade-craft'],
                'art_styles': ['functional', 'traditional'],
                'price_range': (40, 200),
                'materials': [
                    'Organic cotton, natural indigo dye, sustainable mordants',
                    'Recycled fabrics, natural dyes, sustainable thread',
                    'Handmade paper, natural pigments, eco-friendly binders',
                    'Sustainable fibers, natural dyes, traditional techniques'
                ]
            },
            'aisha_patel': {
                'categories': ['natural_sustainable'],
                'image_patterns': ['upcycled-eco-product', 'zero-waste-eco-product'],
                'art_styles': ['mixed_media', 'sculptural'],
                'price_range': (60, 300),
                'materials': [
                    'Upcycled materials, natural finishes, eco-friendly adhesives',
                    'Zero-waste materials, natural fibers, sustainable practices',
                    'Recycled components, sustainable binders, natural elements',
                    'Discarded materials, eco-friendly processes, sustainable techniques'
                ]
            }
        }

        # Artist statement templates
        statement_templates = [
            "This piece represents the harmony between nature and human creativity, using materials that give back to the earth.",
            "Giving new life to discarded materials, this artwork celebrates the beauty of sustainable practices.",
            "Created with environmental consciousness, this piece tells a story of renewal and responsible creativity.",
            "This artwork demonstrates that beauty and sustainability can coexist, inspiring others to make eco-conscious choices.",
            "Using traditional techniques with modern sustainable practices, this piece honors both craftsmanship and environmental responsibility.",
            "Transforming waste into wonder, this creation challenges our perception of beauty and sustainability.",
            "This piece explores the relationship between human creativity and environmental responsibility.",
            "Celebrating the circular economy, this artwork gives new purpose to materials that would otherwise be discarded."
        ]

        images_dir = options['images_dir']
        created_count = 0

        # Get all image files
        if not os.path.exists(images_dir):
            self.stdout.write(
                self.style.ERROR(f'Images directory not found: {images_dir}')
            )
            return

        image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png'))]
        
        # Assign images to artists
        for artist in artists:
            artist_data = artist_assignments.get(artist.username)
            if not artist_data:
                continue
                
            # Find images that match this artist's patterns
            artist_images = []
            for image_file in image_files:
                if any(pattern in image_file.lower() for pattern in artist_data['image_patterns']):
                    artist_images.append(image_file)
            
            # Limit to 8-10 products per artist
            artist_images = artist_images[:random.randint(8, 10)]
            
            self.stdout.write(f'\nAssigning {len(artist_images)} products to {artist.get_full_name()}...')
            
            for image_file in artist_images:
                # Determine category and art style
                category = random.choice(artist_data['categories'])
                art_style = random.choice(artist_data['art_styles'])
                
                # Generate title from filename
                title = self.generate_title_from_filename(image_file, category)
                
                # If title is None, it means the image is for a showcase/educational product, skip it
                if title is None:
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠ Skipping image: {image_file} (likely a showcase/educational product)')
                    )
                    continue
                
                # Generate description
                description = self.generate_description(title, category, artist.get_full_name())
                
                # Generate price based on artist's range
                min_price, max_price = artist_data['price_range']
                price = Decimal(str(random.randint(min_price, max_price)))
                
                # Get materials and statement
                materials = random.choice(artist_data['materials'])
                artist_statement = random.choice(statement_templates)
                
                # Generate dimensions
                dimensions = self.generate_dimensions(category)
                
                # Random sustainability rating (3-5 for eco-art)
                sustainability_rating = random.randint(3, 5)
                
                # Create the product
                product = Product.objects.create(
                    title=title,
                    description=description,
                    price=price,
                    category=category,
                    art_style=art_style,
                    materials=materials,
                    dimensions=dimensions,
                    location=artist.profile.location,
                    owner=artist,
                    artist_statement=artist_statement,
                    sustainability_rating=sustainability_rating
                )
                
                # Set the image
                image_path = os.path.join(images_dir, image_file)
                with open(image_path, 'rb') as img_file:
                    from django.core.files import File
                    product.image.save(image_file, File(img_file), save=True)
                
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ Created: {product.title} (${product.price})')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n🎨 Successfully created {created_count} eco-art products!')
        )
        self.stdout.write(
            self.style.SUCCESS('✨ Each artist now has their own collection of sustainable artwork!')
        )

    def generate_title_from_filename(self, filename, category):
        """Generate a meaningful title from the filename"""
        # Remove extension and common prefixes
        name = filename.replace('.webp', '').replace('.jpg', '').replace('.jpeg', '').replace('.png', '')
        
        # Skip showcase/educational images that shouldn't be products
        if any(skip_word in name.lower() for skip_word in ['showcase', 'information', 'transport', 'celebration', 'guide']):
            return None
        
        # Replace hyphens and underscores with spaces
        name = name.replace('-', ' ').replace('_', ' ')
        
        # Capitalize words
        name = ' '.join(word.capitalize() for word in name.split())
        
        # Create more artistic titles based on the actual content
        if 'recycled-metal' in filename.lower():
            if 'owl' in filename.lower():
                return "Recycled Metal Owl Sculpture"
            elif 'elephant' in filename.lower():
                return "Recycled Metal Elephant Head"
            elif 'scorpion' in filename.lower():
                return "Recycled Metal Scorpion Garden Sculpture"
            elif 'sheep' in filename.lower():
                return "Recycled Spark Plug Sheep Sculpture"
            elif 'angler-fish' in filename.lower():
                return "Steampunk Angler Fish Metal Sculpture"
            else:
                return f"Recycled Metal {name.split()[-1].title()} Sculpture"
        
        elif 'eco-jewelry' in filename.lower() or 'jewelry' in filename.lower():
            if 'bracelet' in filename.lower():
                return "Sustainable Canyon Clear Bracelet"
            elif 'reclaimed-wood' in filename.lower():
                return "Reclaimed Wood Jewelry Set"
            else:
                return f"Sustainable {name.split()[-1].title()} Jewelry"
        
        elif 'eco-wall-art' in filename.lower():
            return f"Eco Wall Art - {name.split()[-1].title()} Collection"
        
        elif 'eco-home-decor' in filename.lower():
            return f"Handmade Eco Home Decor - {name.split()[-1].title()}"
        
        elif 'handmade-eco-product' in filename.lower():
            return f"Handmade Eco Product - {name.split()[-1].title()}"
        
        elif 'handmade-clay' in filename.lower():
            return "Handmade Clay Towers Sculpture"
        
        elif 'sustainable-clothing' in filename.lower():
            return f"Sustainable Clothing - {name.split()[-1].title()} Collection"
        
        elif 'artisan-handmade' in filename.lower():
            return f"Artisan Handmade {name.split()[-1].title()}"
        
        elif 'handmade-craft' in filename.lower():
            return f"Handmade Craft {name.split()[-1].title()}"
        
        elif 'natural-eco-paints' in filename.lower():
            return "Natural Eco Paints Collection"
        
        elif 'upcycled-eco-product' in filename.lower():
            return f"Upcycled Eco Product - {name.split()[-1].title()}"
        
        elif 'zero-waste-eco-product' in filename.lower():
            return f"Zero Waste Eco Product - {name.split()[-1].title()}"
        
        elif 'fine-art' in filename.lower():
            return "Sustainable Fine Art Piece"
        
        elif 'collage' in filename.lower():
            return "Three Waves Collage Art"
        
        elif 'vulnerability' in filename.lower():
            return "Universal Vulnerability Art"
        
        # Default fallback
        return f"Eco Art {name.split()[-1].title()}"

    def generate_description(self, title, category, artist_name):
        """Generate a description based on the title, category, and artist"""
        descriptions = {
            'eco_jewelry': f"Beautiful {title.lower()} crafted by {artist_name} with sustainable materials and eco-conscious practices. Each piece is unique and tells a story of environmental responsibility.",
            'recycled_sculptures': f"Stunning {title.lower()} created by {artist_name} entirely from recycled materials. This piece transforms waste into wonder, showcasing the beauty of sustainable art.",
            'wall_art': f"Contemporary {title.lower()} by {artist_name} that combines artistic expression with environmental consciousness. Perfect for adding sustainable beauty to any space.",
            'home_decor': f"Handcrafted {title.lower()} by {artist_name} made with natural materials and sustainable practices. Each piece brings eco-friendly elegance to your home.",
            'handmade_artisan': f"Artisan-crafted {title.lower()} by {artist_name} using traditional techniques and sustainable materials. A testament to both craftsmanship and environmental responsibility.",
            'natural_sustainable': f"Natural {title.lower()} by {artist_name} created with organic materials and sustainable processes. This piece celebrates the harmony between art and nature.",
            'sustainable_fashion': f"Stylish {title.lower()} by {artist_name} made from sustainable materials and ethical production practices. Fashion that cares for the planet.",
            'showcase_educational': f"Educational {title.lower()} by {artist_name} designed to inspire and inform about sustainable art practices. Perfect for galleries and learning spaces."
        }
        return descriptions.get(category, f"Beautiful {title.lower()} by {artist_name} created with sustainable materials and eco-conscious practices.")

    def generate_dimensions(self, category):
        """Generate appropriate dimensions based on category"""
        dimensions = {
            'eco_jewelry': ['18" necklace length', '7.5" bracelet circumference', 'Adjustable ring size'],
            'recycled_sculptures': ['24" x 18" x 12"', '16" x 12" x 8"', 'Variable installation size'],
            'wall_art': ['36" x 24"', '48" x 36"', '24" x 18"'],
            'home_decor': ['12" x 8" x 6"', '8" x 6" x 4"', 'Variable size'],
            'handmade_artisan': ['24" x 24"', '18" x 18"', 'Variable dimensions'],
            'natural_sustainable': ['Set of 6 colors', 'Various sizes', 'Custom dimensions'],
            'sustainable_fashion': ['Various sizes available', 'One size fits most', 'Custom sizing'],
            'showcase_educational': ['Variable installation size', 'Educational display', 'Custom dimensions']
        }
        return random.choice(dimensions.get(category, ['Variable dimensions'])) 