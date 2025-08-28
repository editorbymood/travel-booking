from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import uuid


class TravelOption(models.Model):
    """Model representing a travel option (Flight/Train/Bus)"""
    
    TRAVEL_TYPES = [
        ('Flight', 'Flight'),
        ('Train', 'Train'),
        ('Bus', 'Bus'),
    ]
    
    travel_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=10, choices=TRAVEL_TYPES)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    available_seats = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['datetime']
    
    def __str__(self):
        return f"{self.type} from {self.source} to {self.destination} on {self.datetime.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def has_available_seats(self):
        return self.available_seats > 0


class Booking(models.Model):
    """Model representing a booking made by a user"""
    
    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE, related_name='bookings')
    number_of_seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Confirmed')
    
    class Meta:
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"Booking {str(self.booking_id)[:8]} - {self.user.username} - {self.travel_option.type}"
    
    def save(self, *args, **kwargs):
        # Calculate total price based on number of seats and travel option price
        if not self.total_price:
            self.total_price = self.number_of_seats * self.travel_option.price
        super().save(*args, **kwargs)
    
    def cancel(self):
        """Cancel the booking and return seats to travel option"""
        if self.status == 'Confirmed':
            self.status = 'Cancelled'
            self.travel_option.available_seats += self.number_of_seats
            self.travel_option.save()
            self.save()
            return True
        return False
