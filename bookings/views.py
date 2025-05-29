from django.shortcuts import render, redirect
from .models import Customer, Booking, Table
from .forms import PublicBookingForm
from django.utils import timezone
from django.contrib import messages
from django.db import IntegrityError
from datetime import datetime

# from django.core.exceptions import ValidationError


def public_booking_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        number_of_guests = int(request.POST.get('number_of_guests'))
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        special_requests = request.POST.get('special_requests', '')

        try:
            # 🔍 Try to find the customer by email or phone
            customer = (
                Customer.objects.filter(email=email).first() or
                Customer.objects.filter(phone_number=phone).first()
            )

            if customer:
                # ✏️ Update info if name has changed
                if customer.name != name:
                    customer.name = name
                    customer.save()
            else:
                # 🆕 Create new if not found
                customer = Customer.objects.create(
                    name=name,
                    email=email,
                    phone_number=phone
                )

        except IntegrityError:
            messages.error(
                request,
                "A customer with this phone or email already exists."
            )
            return redirect('public_booking')  # or wherever your booking form is

        booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()

        # 🧠 Find an available table

        conflicting_bookings = Booking.objects.filter(
            booking_date=booking_date_obj,
            booking_time=booking_time
        ).values_list('table_id', flat=True)

        # ✅ Filter tables that can accommodate the number of guests and are not booked at the same time

        available_tables = (
            Table.objects
            .filter(seats__gte=number_of_guests)
            .exclude(id__in=conflicting_bookings)
            .order_by('seats')
        )
        # 🛑 If no tables are available, show an error message

        if not available_tables.exists():
            messages.error(
                request,
                "No tables available for the selected date and time."
            )
            return redirect('public_booking')

        # ✅ Select the first available table
        table = available_tables.first()

    # ✅ Create the booking

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
        # If GET request, render the booking form
        form = PublicBookingForm()
        context = {'form': form}
        return render(request, 'bookings/booking_form.html', context)

    return render(request, 'bookings/booking_form.html')


def booking_success(request):
    return render(request, 'bookings/booking_success.html')
