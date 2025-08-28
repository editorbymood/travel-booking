#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
"

# Seed data if no travel options exist
python manage.py shell -c "
from bookings.models import TravelOption
if not TravelOption.objects.exists():
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'seed_data', '--count', '30'])
    print('Sample data created')
else:
    print('Sample data already exists')
"
