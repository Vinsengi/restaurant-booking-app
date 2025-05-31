from django.shortcuts import render, redirect
from .models import Customer, Booking, Table
from .forms import PublicBookingForm
from django.contrib import messages
from django.db import IntegrityError, transaction
from datetime import datetime, timedelta
from django.db.models import Q
from django.urls import reverse
from .email_utils import send_booking_email
from urllib.parse import urlencode
import logging
# Initialize logger
logger = logging.getLogger(__name__)


def public_booking_view(request):
    if request.method == 'POST':
        form = PublicBookingForm(request.POST)
        if form.is_valid():
            # Extract cleaned data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone_number']
            booking_date = form.cleaned_data['booking_date']
            booking_time = form.cleaned_data['booking_time']
            number_of_guests = form.cleaned_data['number_of_guests']
            special_requests = form.cleaned_data.get('special_requests', '')
     
            # Log the booking attempt
            logger.info(
                f"Booking attempt: {name}, {email}, {phone}, "
                f"{booking_date}, at {booking_time}, for {number_of_guests} guests, "
                f"Special Requests: {special_requests}"
            )

            try:
                with transaction.atomic():
                    # 🔍 Customer lookup or creation
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
                            name=name, email=email, phone_number=phone
                        )

                    # ⏳ Define time window: +/- 2 hours
                    start_time = (
                        datetime.combine(booking_date, booking_time) -
                        timedelta(hours=2)
                    ).time()
                    end_time = (
                        datetime.combine(booking_date, booking_time) +
                        timedelta(hours=2)
                    ).time()

                    # ❌ Get conflicting bookings in the window
                    conflicting_table_ids = Booking.objects.filter(
                        booking_date=booking_date,
                        booking_time__gte=start_time,
                        booking_time__lte=end_time
                    ).values_list('table_id', flat=True)

                    # ✅ Find available tables not in conflict
                    available_tables = Table.objects.filter(
                        seats__gte=number_of_guests
                    ).exclude(
                        id__in=conflicting_table_ids
                    ).order_by('seats')

                    if not available_tables.exists():
                        messages.error(
                            request,
                            "Sorry, all tables are booked at that time. "
                            "Please try another slot "
                            "(minimum 2-hour "
                            "interval)."
                        )
                        return render(
                            request,
                            'bookings/booking_form.html',
                            {
                                'form': form,
                                'available_tables': [],
                                'conflicting_table_ids': list(
                                    conflicting_table_ids
                                ),
                                'no_availability': True
                            }
                        )

                    selected_table = available_tables.first()

                    # 📝 Create the booking
                    new_booking = Booking.objects.create(
                        customer=customer,
                        table=selected_table,
                        number_of_guests=number_of_guests,
                        booking_date=booking_date,
                        booking_time=booking_time,
                        special_requests=special_requests
                    )
                    logger.info(
                        f"Booking created successfully: {new_booking.id} "
                        f"for {customer.name} at {booking_date} "
                        f"at {booking_time} for {number_of_guests} guests."
                        f"on Table: {selected_table.table_number}"
                    )
                    try:
                        send_booking_email(new_booking, customer)
                    except Exception as e:
                        logger.exception("Email sending failed.")
                        messages.warning(
                            request,
                            "Booking confirmed, but there was an issue sending the confirmation email."
                        )
                    else:
                        messages.success(
                            request,
                            f"Your booking for {booking_date} at {booking_time.strftime('%H:%M')} was successful! A confirmation email has been sent to {email}."
                    )
                  
                    base_url = reverse('booking_success')
                    query_string = urlencode({'booking_id': new_booking.id})
                    booking_success_url = f"{base_url}?{query_string}"
                    return redirect(booking_success_url)

            except IntegrityError:
                logger.exception("Booking failed due to integrity error.")
                messages.error(
                    request,
                    (
                        "Oops! That table was just booked by someone else. "
                        "Please try again."
                    )
                )
                return redirect('public_booking')
        else:
            logger.warning("Invalid form submission.")
            messages.error(request, "Please correct the errors below.")
            return render(
                request,
                'bookings/booking_form.html',
                {'form': form}
            )
    else:
        form = PublicBookingForm()
        return render(request, 'bookings/booking_form.html', {
            'form': form,
            'available_tables': None,
            'conflicting_table_ids': [],
            'no_availability': False
        })


def booking_success(request):
    booking_id = request.GET.get('booking_id')
    booking = None
    if booking_id:
        try:
            booking = (
                Booking.objects
                .select_related('table')
                .get(
                    id=booking_id
                )
            )
            logger.info(
                f"Booking success view accessed for booking ID: {booking_id}"
            )
        except Booking.DoesNotExist:
            logger.warning(
                f"Booking ID {booking_id} not found."
            )
            booking = None
    return render(
        request,
        'bookings/booking_success.html',
        {'booking': booking}
    )


def home(request):
    return render(request, 'bookings/home.html')
