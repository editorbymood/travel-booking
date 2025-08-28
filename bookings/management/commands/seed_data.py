from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from bookings.models import TravelOption
import random


class Command(BaseCommand):
    help = 'Seed the database with sample travel options'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of travel options to create (default: 50)',
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Sample data
        cities = [
            'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
            'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
            'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte',
            'San Francisco', 'Indianapolis', 'Seattle', 'Denver', 'Boston',
            'Washington DC', 'Nashville', 'Oklahoma City', 'Las Vegas', 'Portland'
        ]
        
        travel_types = ['Flight', 'Train', 'Bus']
        
        # Clear existing data
        TravelOption.objects.all().delete()
        
        created_count = 0
        
        for i in range(count):
            # Random source and destination (ensure they're different)
            source = random.choice(cities)
            destination = random.choice([city for city in cities if city != source])
            
            # Random travel type
            travel_type = random.choice(travel_types)
            
            # Random datetime (between now and 60 days from now)
            start_date = timezone.now()
            end_date = start_date + timedelta(days=60)
            random_date = start_date + timedelta(
                seconds=random.randint(0, int((end_date - start_date).total_seconds()))
            )
            
            # Price based on travel type and distance simulation
            base_prices = {
                'Flight': (150, 800),
                'Train': (50, 300),
                'Bus': (25, 150)
            }
            
            min_price, max_price = base_prices[travel_type]
            price = round(random.uniform(min_price, max_price), 2)
            
            # Random available seats
            seat_ranges = {
                'Flight': (50, 200),
                'Train': (100, 400),
                'Bus': (30, 60)
            }
            
            min_seats, max_seats = seat_ranges[travel_type]
            available_seats = random.randint(min_seats, max_seats)
            
            # Create travel option
            travel_option = TravelOption.objects.create(
                type=travel_type,
                source=source,
                destination=destination,
                datetime=random_date,
                price=price,
                available_seats=available_seats
            )
            
            created_count += 1
            
            if created_count % 10 == 0:
                self.stdout.write(f'Created {created_count} travel options...')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} travel options!'
            )
        )
        
        # Display some statistics
        flight_count = TravelOption.objects.filter(type='Flight').count()
        train_count = TravelOption.objects.filter(type='Train').count()
        bus_count = TravelOption.objects.filter(type='Bus').count()
        
        self.stdout.write(f'Statistics:')
        self.stdout.write(f'  Flights: {flight_count}')
        self.stdout.write(f'  Trains: {train_count}')
        self.stdout.write(f'  Buses: {bus_count}')
        self.stdout.write(f'  Total: {created_count}')
