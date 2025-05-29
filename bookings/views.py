from django.shortcuts import render, redirect
from .models import Customer, Booking, Table
from .forms import PublicBookingForm
from django.contrib import messages
from django.db import IntegrityError
from datetime import datetime


def public_booking_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        special_requests = request.POST.get('special_requests', '')
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')

        # Validate number of guests
        try:
            number_of_guests = int(request.POST.get('number_of_guests', 0))
            if number_of_guests <= 0:
                messages.error(request, "Please fill the whole form and Please enter a valid number of guests.")
                return redirect('public_booking')
        except (ValueError, TypeError):
            messages.error(request, "Invalid number of guests.")
            return redirect('public_booking')

        # Parse and validate booking date
        try:
            booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            messages.error(request, "Invalid booking date format.")
            return redirect('public_booking')

        # Find or create customer
        try:
            customer = (
                Customer.objects.filter(email=email).first() or
                Customer.objects.filter(phone_number=phone).first()
            )

            if customer:
                if customer.name != name:
                    customer.name = name
                    customer.save()
            else:
                customer = Customer.objects.create(
                    name=name,
                    email=email,
                    phone_number=phone
                )
        except IntegrityError:
            messages.error(request, "A customer with this phone or email already exists.")
            return redirect('public_booking')

        # Find available table
        conflicting_bookings = Booking.objects.filter(
            booking_date=booking_date_obj,
            booking_time=booking_time
        ).values_list('table_id', flat=True)

        available_tables = Table.objects.filter(
            seats__gte=number_of_guests
        ).exclude(
            id__in=conflicting_bookings
        ).order_by('seats')

        if not available_tables.exists():
            messages.error(
                request,
                "So sorry, no tables are available for the selected date and time."
            )
            return redirect('public_booking')

        table = available_tables.first()

        # Create booking
        Booking.objects.create(
            customer=customer,
            table=table,
            number_of_guests=number_of_guests,
            booking_date=booking_date_obj,
            booking_time=booking_time,
            special_requests=special_requests
        )

        return redirect('booking_success')

    else:
        form = PublicBookingForm()
        return render(request, 'bookings/booking_form.html', {'form': form})


def booking_success(request):
    return render(request, 'bookings/booking_success.html')
