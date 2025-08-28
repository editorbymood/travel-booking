from django.contrib import admin
from .models import TravelOption, Booking


@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ['travel_id', 'type', 'source', 'destination', 'datetime', 'price', 'available_seats']
    list_filter = ['type', 'source', 'destination', 'datetime']
    search_fields = ['source', 'destination', 'type']
    ordering = ['datetime']
    readonly_fields = ['travel_id']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'travel_option', 'number_of_seats', 'total_price', 'booking_date', 'status']
    list_filter = ['status', 'booking_date', 'travel_option__type']
    search_fields = ['user__username', 'user__email', 'travel_option__source', 'travel_option__destination']
    ordering = ['-booking_date']
    readonly_fields = ['booking_id', 'booking_date', 'total_price']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['user', 'travel_option', 'number_of_seats']
        return self.readonly_fields
