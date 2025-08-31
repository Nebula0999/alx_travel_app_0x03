from django.core.management.base import BaseCommand
from listings.models import User, Listing, Booking, Review
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings, users, bookings, and reviews.'

    def handle(self, *args, **kwargs):
        # Create sample users
        users = []
        for i in range(3):
            user, created = User.objects.get_or_create(
                username=f'user{i}',
                defaults={
                    'first_name': f'First{i}',
                    'last_name': f'Last{i}',
                    'phone_number': f'12345678{i}',
                    'role': 'host' if i == 0 else 'guest',
                }
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS('Sample users created.'))

        # Create sample listings
        listings = []
        for i in range(5):
            listing, created = Listing.objects.get_or_create(
                title=f'Listing {i}',
                defaults={
                    'description': f'Description for listing {i}',
                    'price_per_night': random.randint(50, 200),
                    'location': f'City {i}',
                    'host': users[0],
                }
            )
            listings.append(listing)
        self.stdout.write(self.style.SUCCESS('Sample listings created.'))

        # Create sample bookings
        for i in range(5):
            Booking.objects.get_or_create(
                listing=listings[i],
                user=users[1],
                defaults={
                    'start_date': timezone.now().date(),
                    'end_date': timezone.now().date(),
                }
            )
        self.stdout.write(self.style.SUCCESS('Sample bookings created.'))

        # Create sample reviews
        for i in range(5):
            Review.objects.get_or_create(
                listing=listings[i],
                user=users[2],
                defaults={
                    'rating': random.randint(1, 5),
                    'comment': f'Review comment {i}',
                }
            )
        self.stdout.write(self.style.SUCCESS('Sample reviews created.'))