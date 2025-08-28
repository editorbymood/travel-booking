from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Booking, TravelOption


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form with Bootstrap styling"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form with additional fields"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class TravelOptionFilterForm(forms.Form):
    """Form for filtering travel options"""
    source = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Source city', 'class': 'form-control'})
    )
    destination = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Destination city', 'class': 'form-control'})
    )
    travel_type = forms.ChoiceField(
        choices=[('', 'All Types')] + TravelOption.TRAVEL_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    min_price = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Min price', 'class': 'form-control', 'step': '0.01'})
    )
    max_price = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Max price', 'class': 'form-control', 'step': '0.01'})
    )


class BookingForm(forms.ModelForm):
    """Form for creating a new booking"""
    
    class Meta:
        model = Booking
        fields = ['number_of_seats']
        
    def __init__(self, *args, **kwargs):
        self.travel_option = kwargs.pop('travel_option', None)
        super().__init__(*args, **kwargs)
        
        self.fields['number_of_seats'].widget.attrs.update({
            'class': 'form-control',
            'min': '1',
            'max': str(self.travel_option.available_seats) if self.travel_option else '1'
        })
        
        if self.travel_option:
            self.fields['number_of_seats'].help_text = f"Maximum {self.travel_option.available_seats} seats available"

    def clean_number_of_seats(self):
        number_of_seats = self.cleaned_data['number_of_seats']
        
        if self.travel_option and number_of_seats > self.travel_option.available_seats:
            raise forms.ValidationError(
                f"Only {self.travel_option.available_seats} seats are available for this travel option."
            )
        
        return number_of_seats


class BookingSearchForm(forms.Form):
    """Form for searching user's bookings"""
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Booking.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    travel_type = forms.ChoiceField(
        choices=[('', 'All Types')] + TravelOption.TRAVEL_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
