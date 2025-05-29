from django.shortcuts import render, redirect
from .forms import BookingForm


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
