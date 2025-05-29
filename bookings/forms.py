from django import forms
from .models import Booking, Customer, Table


#  Admin/ Internal form
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'customer',
            'number_of_guests',
            'booking_date',
            'booking_time',
            'special_requests',
        ]
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Any special requests or notes'
                }
            ),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'number_of_guests': forms.NumberInput(
                attrs={'min': 1, 'class': 'form-control'}
            ),
            'booking_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'customer': 'Customer Name',
            'number_of_guests': 'Number of Guests',
            'table': 'Table Number',
            'booking_date': 'Booking Date',
            'booking_time': 'Booking Time',
            'special_requests': 'Special Requests (if any)',
        }
        help_texts = {
            'customer': 'Select or create a customer for this booking.',
            'number_of_guests': 'Enter the number of guests for this booking.',
            'table': 'Select the table for this booking.',
            'booking_date': 'Select the date for the booking.',
            'booking_time': 'Select the time for the booking.',
            'special_requests': 'Any special requests or notes for the booking.',
        }
        error_messages = {
            'customer': {
                'required': 'Please select a customer for the booking.',
            },
            'number_of_guests': {
                'required': 'Please enter the number of guests.',
                'invalid': 'Please enter a valid number of guests.',
            },
            
            'booking_date': {
                'required': 'Please select a booking date.',
                'invalid': 'Please enter a valid date.',
            },
            'booking_time': {
                'required': 'Please select a booking time.',
                'invalid': 'Please enter a valid time.',
            },
        }


class PublicBookingForm(forms.Form):
    name = forms.CharField(
        label="Your Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )

    phone_number = forms.CharField(
        label="Phone Number",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    number_of_guests = forms.IntegerField(
        label="Number of Guests",
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Minimum of 1 guest required"
    )

    booking_date = forms.DateField(
        label="Booking Date",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    booking_time = forms.TimeField(
        label="Booking Time",
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        }),
        help_text="Format: HH:MM"
    )

    special_requests = forms.CharField(
        label="Special Requests (optional)",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        })
    )
