from django.db import models
from django.utils import timezone
from django.conf import settings
from datetime import datetime
import uuid

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True) # Assuming phone numbers are unique to each customer
    created_at = models.DateTimeField(auto_now_add=True)    # Automatically set the creation time when a customer is created
    updated_at = models.DateTimeField(auto_now=True)         # Automatically update the time when a customer is modified

    def __str__(self):
        return f"{self.name} ({self.email})"


class Table(models.Model):
    table_number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)    
    created_at = models.DateTimeField(auto_now_add=True)    # Automatically set the creation time when a table is created
    updated_at = models.DateTimeField(auto_now=True)         # Automatically update the time when a table is modified

    def __str__(self):
        return f"Table {self.table_number} - Seats: {self.seats} - {'Available' if self.is_available else 'Not Available'}"


class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    number_of_guests = models.PositiveIntegerField(default=1)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    booking_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)   # Automatically update the time when a booking is modified 
    status = models.CharField(max_length=20, choices=[('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='confirmed')     # Status can be 'confirmed' or 'cancelled'
    special_requests = models.TextField(blank=True, null=True)  # Optional field for any special requests by the customer
    cancellation_token = models.UUIDField(default=uuid.uuid4, unique=True, null=True, blank=True)


    def __str__(self):
        return (
            f"Booking for {self.customer} at {self.booking_date} - "
            f"Table {self.table.table_number} - Status: {self.status}"
        )

    class Meta:
        ordering = ['-booking_date']    # Orders bookings by booking date in descending order
        unique_together = ('table', 'booking_date', 'booking_time')  # Ensures that a table cannot be booked for the same date and time by different customers
    # Automatically set the status based on the booking date

    def save(self, *args, **kwargs):
        # Convert string to date object if necessary
        if isinstance(self.booking_date, str):
            try:
                self.booking_date = datetime.strptime(self.booking_date, "%Y-%m-%d").date()
            except ValueError:
                self.booking_date = timezone.now().date()  # fallback to today
         
        # Automatically set the status based on the booking date
        # if self.booking_date < timezone.now().date():
        #     self.status = 'cancelled'  # Automatically cancel bookings in the past 
        super().save(*args, **kwargs)


class Cancellation(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    cancellation_date = models.DateTimeField(auto_now_add=True)  # Automatically set the cancellation date when a cancellation is created
    reason = models.TextField(blank=True, null=True)  # Optional field for the reason of cancellation
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return (
            f"Cancellation for {self.booking} on {self.cancellation_date} - "
            f"Reason: {self.reason or 'No reason provided'}"
        )


class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        "Image",
        upload_to='menu_images',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['name']  # Orders menu items by name in ascending order
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return self.name


class Feedback(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveIntegerField()  # Assuming a rating scale of 1 to 5
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='feedbacks', null=True, blank=True)

    # Adding a foreign key to Customer to link feedback to the customer who made the booking

    def __str__(self):
        return (
            f"Feedback for {self.booking} - Rating: {self.rating} - "
            f"Comments: {self.comments or 'No comments'}"
        )

    class Meta:
        ordering = ['-created_at']  # Orders feedback by creation date in descending order

    def save(self, *args, **kwargs):
        # Automatically set the rating to 1 if not provided
        if self.rating is None:
            self.rating = 5
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    customer  = models.ForeignKey(
        Customer,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='contact_messages'
    )
    name      = models.CharField(max_length=100)
    email     = models.EmailField()
    phone_number = models.CharField(
        max_length=15,
        null=True,      # allow existing rows to have NULL
        blank=True,     # allow form-level blank
        unique=True    # don’t enforce uniqueness just yet
    )
    message   = models.TextField()
    submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} <{self.email}> @ {self.submitted:%Y-%m-%d %H:%M}"