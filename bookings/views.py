from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Booking, Table, Cancellation, MenuItem
from .forms import PublicBookingForm
from django.contrib import messages
from django.db import IntegrityError, transaction
from datetime import datetime, timedelta
from django.db.models import Q
from django.urls import reverse
from .email_utils import send_booking_email
from urllib.parse import urlencode
from django.http import HttpResponse
from django.core.paginator import Paginator

import logging
# Initialize logger
logger = logging.getLogger(__name__)


def public_booking_view(request):
    menu_item_id = request.GET.get('menu_item')
    menu_item = None
    if menu_item_id:
        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)
        except MenuItem.DoesNotExist:
            menu_item = None

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
                                'no_availability': True,
                                'menu_item': menu_item,
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
                    # Cancellation.objects.create(
                    #     booking=new_booking)
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
            'no_availability': False,
            'menu_item': menu_item,
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


def about_view(request):
    return render(request, 'bookings/about.html')


def contact_view(request):
    return render(request, 'bookings/contact.html')


def menu_view(request):
    menu_items = MenuItem.objects.filter(is_available=True).order_by('name')
    paginator = Paginator(menu_items, 3)  # Show 6 items per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'bookings/menu.html', {'page_obj': page_obj})


# def cancel_booking_view(request):
#     token = request.GET.get('token')
#     if not token:
#         return HttpResponseNotFound("Invalid or missing cancellation token.")

#     try:
#         cancellation = Cancellation.objects.select_related('booking').get(token=token)
#         booking = cancellation.booking
#         booking.delete()  # or mark as canceled instead
#         messages.success(request, "Your booking has been successfully canceled.")
#     except Cancellation.DoesNotExist:
#         messages.error(request, "Invalid cancellation token.")

#     return render(request, 'bookings/cancel_booking.html')


# def cancel_booking_view(request):
#     token = request.GET.get('token')
#     booking = get_object_or_404(Booking, cancellation_token=token)

#     if request.method == 'POST':
#         Cancellation.objects.create(booking=booking, reason="Cancelled by user")
#         messages.success(request, "Your booking has been cancelled.")
#         return render(request, 'bookings/cancel_success.html')

#     return render(request, 'bookings/cancel_booking.html', {'booking': booking})


def cancel_booking_view(request):
    token = request.GET.get('token')
    booking = get_object_or_404(Booking, cancellation_token=token)

    if request.method == 'POST':
        # Prevent double cancellation
        if not hasattr(booking, 'cancellation'):
            Cancellation.objects.create(booking=booking, reason="Cancelled by user")
            messages.success(request, "Your booking has been successfully canceled.")
        else:
            messages.info(request, "This booking has already been canceled.")

        return redirect('cancel_success')

    return render(request, 'bookings/cancel_booking.html', {'booking': booking})


def cancel_success_view(request):
    return render(request, 'bookings/cancel_success.html')


def view_bookings(request):
    bookings = Booking.objects.select_related('customer', 'table').all()
    return render(request, 'bookings/view_bookings.html', {'bookings': bookings})
