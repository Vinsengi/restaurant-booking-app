from django.shortcuts import render, redirect
from .models import Customer, Booking, Table
from .forms import PublicBookingForm
from django.contrib import messages
from django.db import IntegrityError, transaction
from datetime import datetime, timedelta
from django.db.models import Q
from django.urls import reverse


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

                    booking_success_url = (
                        f"{reverse('booking_success')}"
                        f"?booking_id={new_booking.id}"
                    )
                    return redirect(booking_success_url)
            except IntegrityError:
                messages.error(
                    request,
                    (
                        "Oops! That table was just booked by someone else. "
                        "Please try again."
                    )
                )
                return redirect('public_booking')

        else:
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
        except Booking.DoesNotExist:
            booking = None
    return render(
        request,
        'bookings/booking_success.html',
        {'booking': booking}
    )
