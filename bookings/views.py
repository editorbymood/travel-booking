from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.utils import timezone
from .models import TravelOption, Booking
from .forms import (
    CustomUserCreationForm, 
    CustomAuthenticationForm,
    UserProfileForm, 
    TravelOptionFilterForm, 
    BookingForm, 
    BookingSearchForm
)


def home(request):
    """Home page view with recent travel options"""
    recent_options = TravelOption.objects.filter(
        datetime__gte=timezone.now(),
        available_seats__gt=0
    )[:6]
    
    context = {
        'recent_options': recent_options,
    }
    return render(request, 'bookings/home.html', context)


class CustomLoginView(LoginView):
    """Custom login view"""
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class RegisterView(CreateView):
    """User registration view"""
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Account created for {username}! You can now log in.')
        return response


@login_required
def profile_view(request):
    """User profile view and update"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'registration/profile.html', context)


def travel_options_list(request):
    """List and filter travel options"""
    form = TravelOptionFilterForm(request.GET)
    travel_options = TravelOption.objects.filter(
        datetime__gte=timezone.now(),
        available_seats__gt=0
    )
    
    if form.is_valid():
        # Apply filters
        if form.cleaned_data['source']:
            travel_options = travel_options.filter(
                source__icontains=form.cleaned_data['source']
            )
        
        if form.cleaned_data['destination']:
            travel_options = travel_options.filter(
                destination__icontains=form.cleaned_data['destination']
            )
        
        if form.cleaned_data['travel_type']:
            travel_options = travel_options.filter(
                type=form.cleaned_data['travel_type']
            )
        
        if form.cleaned_data['date_from']:
            travel_options = travel_options.filter(
                datetime__date__gte=form.cleaned_data['date_from']
            )
        
        if form.cleaned_data['date_to']:
            travel_options = travel_options.filter(
                datetime__date__lte=form.cleaned_data['date_to']
            )
        
        if form.cleaned_data['min_price']:
            travel_options = travel_options.filter(
                price__gte=form.cleaned_data['min_price']
            )
        
        if form.cleaned_data['max_price']:
            travel_options = travel_options.filter(
                price__lte=form.cleaned_data['max_price']
            )
    
    context = {
        'form': form,
        'travel_options': travel_options,
    }
    return render(request, 'bookings/travel_options_list.html', context)


@login_required
def book_travel(request, travel_id):
    """Book a travel option"""
    travel_option = get_object_or_404(TravelOption, travel_id=travel_id)
    
    if not travel_option.has_available_seats:
        messages.error(request, 'Sorry, this travel option is fully booked.')
        return redirect('travel_options_list')
    
    if request.method == 'POST':
        form = BookingForm(request.POST, travel_option=travel_option)
        if form.is_valid():
            with transaction.atomic():
                # Check if seats are still available
                travel_option.refresh_from_db()
                number_of_seats = form.cleaned_data['number_of_seats']
                
                if number_of_seats > travel_option.available_seats:
                    messages.error(request, 'Sorry, not enough seats available.')
                    return redirect('book_travel', travel_id=travel_id)
                
                # Create booking
                booking = form.save(commit=False)
                booking.user = request.user
                booking.travel_option = travel_option
                booking.total_price = number_of_seats * travel_option.price
                booking.save()
                
                # Update available seats
                travel_option.available_seats -= number_of_seats
                travel_option.save()
                
                messages.success(request, f'Booking confirmed! Booking ID: {str(booking.booking_id)[:8]}')
                return redirect('my_bookings')
    else:
        form = BookingForm(travel_option=travel_option)
    
    context = {
        'form': form,
        'travel_option': travel_option,
    }
    return render(request, 'bookings/book_travel.html', context)


@login_required
def my_bookings(request):
    """View user's bookings with search functionality"""
    form = BookingSearchForm(request.GET)
    bookings = request.user.bookings.all()
    
    if form.is_valid():
        # Apply filters
        if form.cleaned_data['status']:
            bookings = bookings.filter(status=form.cleaned_data['status'])
        
        if form.cleaned_data['travel_type']:
            bookings = bookings.filter(travel_option__type=form.cleaned_data['travel_type'])
        
        if form.cleaned_data['date_from']:
            bookings = bookings.filter(
                travel_option__datetime__date__gte=form.cleaned_data['date_from']
            )
        
        if form.cleaned_data['date_to']:
            bookings = bookings.filter(
                travel_option__datetime__date__lte=form.cleaned_data['date_to']
            )
    
    context = {
        'form': form,
        'bookings': bookings,
    }
    return render(request, 'bookings/my_bookings.html', context)


@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    
    if booking.status == 'Cancelled':
        messages.warning(request, 'This booking is already cancelled.')
        return redirect('my_bookings')
    
    if request.method == 'POST':
        with transaction.atomic():
            if booking.cancel():
                messages.success(request, 'Booking cancelled successfully. Seats have been returned.')
            else:
                messages.error(request, 'Unable to cancel booking.')
        return redirect('my_bookings')
    
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/cancel_booking.html', context)


def travel_option_detail(request, travel_id):
    """View details of a travel option"""
    travel_option = get_object_or_404(TravelOption, travel_id=travel_id)
    
    context = {
        'travel_option': travel_option,
    }
    return render(request, 'bookings/travel_option_detail.html', context)
