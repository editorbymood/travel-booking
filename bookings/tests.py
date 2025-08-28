from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import TravelOption, Booking


class TravelOptionModelTest(TestCase):
    def setUp(self):
        self.travel_option = TravelOption.objects.create(
            type='Flight',
            source='New York',
            destination='Los Angeles',
            datetime=timezone.now() + timedelta(days=7),
            price=299.99,
            available_seats=150
        )

    def test_travel_option_str(self):
        self.assertIn('Flight from New York to Los Angeles', str(self.travel_option))

    def test_has_available_seats(self):
        self.assertTrue(self.travel_option.has_available_seats)
        
        self.travel_option.available_seats = 0
        self.travel_option.save()
        self.assertFalse(self.travel_option.has_available_seats)


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.travel_option = TravelOption.objects.create(
            type='Train',
            source='Boston',
            destination='Washington DC',
            datetime=timezone.now() + timedelta(days=5),
            price=89.99,
            available_seats=200
        )

    def test_booking_creation(self):
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=2
        )
        
        self.assertEqual(booking.total_price, 179.98)  # 2 * 89.99
        self.assertEqual(booking.status, 'Confirmed')

    def test_booking_cancellation(self):
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=3
        )
        
        # Update available seats as would happen in real booking
        self.travel_option.available_seats -= 3
        self.travel_option.save()
        
        # Cancel booking
        success = booking.cancel()
        self.assertTrue(success)
        self.assertEqual(booking.status, 'Cancelled')
        
        # Check seats returned
        self.travel_option.refresh_from_db()
        self.assertEqual(self.travel_option.available_seats, 200)


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.travel_option = TravelOption.objects.create(
            type='Bus',
            source='Seattle',
            destination='Portland',
            datetime=timezone.now() + timedelta(days=3),
            price=45.50,
            available_seats=50
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Travel Booking')

    def test_travel_options_list_view(self):
        response = self.client.get(reverse('travel_options_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Seattle')

    def test_booking_requires_login(self):
        response = self.client.get(
            reverse('book_travel', kwargs={'travel_id': self.travel_option.travel_id})
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_booking_with_login(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('book_travel', kwargs={'travel_id': self.travel_option.travel_id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book Travel')

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())
