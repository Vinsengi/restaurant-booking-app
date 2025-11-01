from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log them in immediately
            messages.success(request, "Account created successfully.")
            return redirect('my_bookings')
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})
