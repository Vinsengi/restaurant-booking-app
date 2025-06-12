from django.contrib import admin
from .models import Customer, Table, Booking, Cancellation, Feedback, MenuItem, ContactMessage
from datetime import datetime, timedelta

# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'seats', 'is_available', 'created_at')
    search_fields = ('table_number',)
    list_filter = ('is_available', 'seats')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'table', 'booking_date', 'booking_time', 'status', 'conflict_warning', 'created_at')
    search_fields = ('customer__email', 'table__table_number')
    list_filter = ('table', 'booking_date')

    def conflict_warning(self, obj):
        if not obj.booking_date or not obj.booking_time:
            return "N/A"
        """
        Check for conflicting bookings within a 2-hour window.
        Returns True if there are conflicting bookings, otherwise False.
        """
        # Check for conflicting bookings within a 2-hour window
        start_time = (
            datetime.combine(obj.booking_date, obj.booking_time) 
            - timedelta(hours=2)
        ).time()
        end_time = (
            datetime.combine(obj.booking_date, obj.booking_time) 
            + timedelta(hours=2)
        ).time()
        # Find bookings that conflict with the current booking
        # within the same date and time range
        conflicting_bookings = Booking.objects.filter(
            booking_date=obj.booking_date,
            booking_time__gte=start_time,
            booking_time__lte=end_time
        ).exclude(id=obj.id)
        return conflicting_bookings.exists()
    conflict_warning.short_description = 'Conflict Warning'
    conflict_warning.boolean = True


@admin.register(Cancellation)
class CancellationAdmin(admin.ModelAdmin):
    list_display = ('booking', 'cancellation_date')
    search_fields = ('booking__customer__email',)
    list_filter = ('cancellation_date',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('customer', 'rating', 'comments', 'created_at')
    search_fields = ('customer__email', 'comment')
    list_filter = ('rating', 'created_at')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available',)
    search_fields = ('name',)
    list_filter = ('is_available',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted')
    list_filter = ('submitted',)
    search_fields = ('name', 'email', 'message')
    date_hierarchy = 'submitted'
    readonly_fields = ('submitted',)