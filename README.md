# Travel Booking System

A complete Django web application for booking travel options including flights, trains, and buses.

## Features

- **User Authentication**: Registration, login, logout, and profile management
- **Travel Options**: Browse and filter flights, trains, and bus tickets
- **Booking System**: Book travel options with seat management
- **Booking Management**: View, filter, and cancel bookings
- **Responsive Design**: Bootstrap-powered responsive UI
- **Admin Interface**: Django admin for managing travel options and bookings

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd travel_booking
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. **Seed sample data**:
   ```bash
   python manage.py seed_data --count 50
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Main site: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Project Structure

```
travel_booking/
├── manage.py
├── requirements.txt
├── README.md
├── travel_booking/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── bookings/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── forms.py
    ├── urls.py
    ├── tests.py
    ├── management/
    │   ├── __init__.py
    │   └── commands/
    │       ├── __init__.py
    │       └── seed_data.py
    ├── migrations/
    ├── templates/
    │   ├── base.html
    │   ├── bookings/
    │   │   ├── home.html
    │   │   ├── travel_options_list.html
    │   │   ├── travel_option_detail.html
    │   │   ├── book_travel.html
    │   │   ├── my_bookings.html
    │   │   └── cancel_booking.html
    │   └── registration/
    │       ├── login.html
    │       ├── register.html
    │       ├── profile.html
    │       └── logged_out.html
    └── static/
        └── css/
            └── style.css
```

## Models

### TravelOption
- `travel_id`: UUID primary key
- `type`: Choice field (Flight/Train/Bus)
- `source`: Source city
- `destination`: Destination city
- `datetime`: Travel date and time
- `price`: Price per seat
- `available_seats`: Number of available seats

### Booking
- `booking_id`: UUID primary key
- `user`: Foreign key to User
- `travel_option`: Foreign key to TravelOption
- `number_of_seats`: Number of seats booked
- `total_price`: Total booking price
- `booking_date`: When booking was made
- `status`: Confirmed/Cancelled

## URLs

- `/` - Home page
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/profile/` - User profile
- `/travel-options/` - Search travel options
- `/travel-options/<uuid:travel_id>/` - Travel option details
- `/travel-options/<uuid:travel_id>/book/` - Book travel option
- `/my-bookings/` - User's bookings
- `/my-bookings/<uuid:booking_id>/cancel/` - Cancel booking
- `/admin/` - Django admin interface

## Management Commands

### seed_data
Populate the database with sample travel options:

```bash
python manage.py seed_data --count 100
```

## Testing

Run tests with:
```bash
python manage.py test
```

## Features in Detail

### Authentication System
- User registration with first name, last name, email
- Login/logout functionality
- Profile update capability
- Login required decorators for protected views

### Travel Options
- Filter by source, destination, travel type, date range, price range
- Responsive card-based display
- Real-time availability checking

### Booking System
- Seat availability validation
- Automatic price calculation
- Transaction-safe booking process
- Booking cancellation with seat return

### UI/UX
- Bootstrap 5 integration
- Responsive design for mobile devices
- Font Awesome icons
- Custom CSS animations
- Alert messages for user feedback

## Technologies Used

- **Backend**: Django 4.2+
- **Frontend**: Bootstrap 5, Font Awesome
- **Database**: SQLite (default, configurable)
- **Styling**: Custom CSS with responsive design

## License

This project is for educational purposes.
