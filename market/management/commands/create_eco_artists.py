from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from market.models import Profile

class Command(BaseCommand):
    help = 'Create 10 diverse eco-artists for the marketplace'

    def handle(self, *args, **options):
        # Define the 10 eco-artists with their details
        artists_data = [
            {
                'username': 'sarah_greenwood',
                'email': 'sarah@greenwoodmetal.com',
                'first_name': 'Sarah',
                'last_name': 'Greenwood',
                'bio': 'Passionate metal sculptor transforming automotive waste into stunning steampunk art. Specializing in recycled metal sculptures that tell stories of environmental consciousness. Each piece is handcrafted from salvaged materials, giving new life to what others discard.',
                'location': 'Portland, Oregon',
                'phone': '(503) 555-0123',
                'social_link': 'https://instagram.com/sarahgreenwoodmetal',
                'specialty': 'Recycled Metal Sculptures & Steampunk Art'
            },
            {
                'username': 'maria_rodriguez',
                'email': 'maria@sustainablecrafts.com',
                'first_name': 'Maria',
                'last_name': 'Rodriguez',
                'bio': 'Artisan jewelry maker and textile artist creating beautiful pieces from natural and recycled materials. Using traditional techniques with modern sustainable practices, I craft unique jewelry that honors both craftsmanship and environmental responsibility.',
                'location': 'Austin, Texas',
                'phone': '(512) 555-0456',
                'social_link': 'https://etsy.com/shop/sustainablecrafts',
                'specialty': 'Sustainable Jewelry & Textiles'
            },
            {
                'username': 'david_chen',
                'email': 'david@earthartstudio.com',
                'first_name': 'David',
                'last_name': 'Chen',
                'bio': 'Contemporary artist exploring the intersection of art and environmental consciousness. My mixed media pieces combine recycled materials with traditional techniques, creating thought-provoking artwork that challenges our relationship with consumption.',
                'location': 'Seattle, Washington',
                'phone': '(206) 555-0789',
                'social_link': 'https://davidchenart.com',
                'specialty': 'Contemporary Wall Art & Mixed Media'
            },
            {
                'username': 'emma_thompson',
                'email': 'emma@greencreations.com',
                'first_name': 'Emma',
                'last_name': 'Thompson',
                'bio': 'Sustainable fashion designer and textile artist using organic materials and ethical production practices. Creating stylish, eco-conscious clothing that proves fashion can be both beautiful and environmentally responsible.',
                'location': 'San Francisco, California',
                'phone': '(415) 555-0321',
                'social_link': 'https://greencreations.com',
                'specialty': 'Sustainable Fashion & Textiles'
            },
            {
                'username': 'alex_rivera',
                'email': 'alex@naturalpaints.com',
                'first_name': 'Alex',
                'last_name': 'Rivera',
                'bio': 'Creator of eco-friendly art supplies and natural paints. Using traditional methods with modern sustainable practices, I produce high-quality art materials that are safe for artists and the environment.',
                'location': 'Boulder, Colorado',
                'phone': '(303) 555-0654',
                'social_link': 'https://naturalpaints.com',
                'specialty': 'Natural Paints & Art Supplies'
            },
            {
                'username': 'lisa_park',
                'email': 'lisa@claycreations.com',
                'first_name': 'Lisa',
                'last_name': 'Park',
                'bio': 'Ceramic artist and home decor creator specializing in handcrafted clay sculptures and sustainable home accessories. Each piece is thrown and glazed using eco-friendly practices, bringing natural beauty to your living space.',
                'location': 'Asheville, North Carolina',
                'phone': '(828) 555-0987',
                'social_link': 'https://claycreations.com',
                'specialty': 'Home Decor & Ceramics'
            },
            {
                'username': 'marcus_johnson',
                'email': 'marcus@reclaimedwood.com',
                'first_name': 'Marcus',
                'last_name': 'Johnson',
                'bio': 'Master woodworker creating stunning sculptures and furniture from reclaimed materials. Giving new purpose to discarded wood, I craft pieces that celebrate the natural beauty and history of salvaged timber.',
                'location': 'Detroit, Michigan',
                'phone': '(313) 555-0123',
                'social_link': 'https://reclaimedwoodart.com',
                'specialty': 'Upcycled Furniture & Wood Art'
            },
            {
                'username': 'sophie_williams',
                'email': 'sophie@digitalecoart.com',
                'first_name': 'Sophie',
                'last_name': 'Williams',
                'bio': 'Digital artist and educator creating eco-conscious digital art and educational content. Using technology to raise awareness about environmental issues while demonstrating how digital art can promote sustainability.',
                'location': 'Portland, Oregon',
                'phone': '(503) 555-0456',
                'social_link': 'https://digitalecoart.com',
                'specialty': 'Digital Eco Art & Educational Content'
            },
            {
                'username': 'carlos_mendez',
                'email': 'carlos@folkartstudio.com',
                'first_name': 'Carlos',
                'last_name': 'Mendez',
                'bio': 'Traditional folk artist preserving cultural heritage through sustainable materials and techniques. Creating authentic folk art pieces that honor traditional craftsmanship while using eco-friendly materials.',
                'location': 'Santa Fe, New Mexico',
                'phone': '(505) 555-0789',
                'social_link': 'https://folkartstudio.com',
                'specialty': 'Folk Art & Traditional Crafts'
            },
            {
                'username': 'aisha_patel',
                'email': 'aisha@zerowasteart.com',
                'first_name': 'Aisha',
                'last_name': 'Patel',
                'bio': 'Installation artist and zero-waste advocate creating large-scale artworks from discarded materials. Transforming waste into wonder, my installations challenge perceptions of beauty and consumption while promoting circular economy principles.',
                'location': 'Brooklyn, New York',
                'phone': '(718) 555-0321',
                'social_link': 'https://zerowasteart.com',
                'specialty': 'Zero-Waste Art & Installations'
            }
        ]

        created_count = 0
        for artist_data in artists_data:
            # Create user
            user, created = User.objects.get_or_create(
                username=artist_data['username'],
                defaults={
                    'email': artist_data['email'],
                    'first_name': artist_data['first_name'],
                    'last_name': artist_data['last_name']
                }
            )
            
            if created:
                # Set password for new users
                user.set_password('ecoartist123')
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Created artist: {user.get_full_name()} ({artist_data["specialty"]})')
                )
                created_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f'Artist already exists: {user.get_full_name()}')
                )

            # Create or update profile
            profile, profile_created = Profile.objects.get_or_create(user=user)
            profile.bio = artist_data['bio']
            profile.location = artist_data['location']
            profile.phone = artist_data['phone']
            profile.social_link = artist_data['social_link']
            profile.save()

            if profile_created:
                self.stdout.write(f'  - Created profile for {user.get_full_name()}')
            else:
                self.stdout.write(f'  - Updated profile for {user.get_full_name()}')

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} new eco-artists!')
        )
        self.stdout.write(
            self.style.SUCCESS('All artists have password: ecoartist123')
        )
        
        # Display summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write('ECO-ARTISTS SUMMARY:')
        self.stdout.write('='*60)
        for artist_data in artists_data:
            self.stdout.write(f'• {artist_data["first_name"]} {artist_data["last_name"]} - {artist_data["specialty"]}')
            self.stdout.write(f'  Location: {artist_data["location"]}')
            self.stdout.write(f'  Username: {artist_data["username"]}')
            self.stdout.write('') 