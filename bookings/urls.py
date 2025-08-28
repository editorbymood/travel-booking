from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Authentication URLs
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('profile/', views.profile_view, name='profile'),
    
    # Travel options URLs
    path('travel-options/', views.travel_options_list, name='travel_options_list'),
    path('travel-options/<uuid:travel_id>/', views.travel_option_detail, name='travel_option_detail'),
    path('travel-options/<uuid:travel_id>/book/', views.book_travel, name='book_travel'),
    
    # Booking management URLs
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('my-bookings/<uuid:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
]
