from django.shortcuts import render, redirect
from .forms import PublicBookingForm
from .models import Booking, Customer


def book_table(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_success')  # We'll create this next
    else:
        form = BookingForm()

    return render(request, 'bookings/booking_form.html', {'form': form})


def booking_success(request):
    return render(request, 'bookings/booking_success.html')


def public_booking_view(request):
    if request.method == 'POST':
        form = PublicBookingForm(request.POST)
        if form.is_valid():
            # Check if customer already exists by email
            email = form.cleaned_data['email']
            customer = Customer.objects.filter(
                email=form.cleaned_data['email']
            ).first()

            if customer:
                # If customer exists, update their details if provided
                customer.name = form.cleaned_data['name']
                customer.phone_number = form.cleaned_data['phone_number']
                customer.save()
            else:
                # If customer does not exist, create a new customer
                customer = Customer.objects.create(
                    email=email,
                    name=form.cleaned_data['name'],
                    phone_number=form.cleaned_data['phone_number']
                )

            # Create the booking
            Booking.objects.create(
                customer=customer,
                table=form.cleaned_data['table'],
                booking_date=form.cleaned_data['booking_date'],
                booking_time=form.cleaned_data['booking_time'],
                number_of_guests=form.cleaned_data['number_of_guests'],
                special_requests=form.cleaned_data['special_requests']
            )

            return redirect('booking_success')
    else:
        form = PublicBookingForm()

    return render(request, 'bookings/booking_form.html', {'form': form})