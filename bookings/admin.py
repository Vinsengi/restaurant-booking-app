from django.contrib import admin
from .models import Customer, Table, Booking, Cancellation, Feedback, MenuItem

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
    list_display = ('customer', 'table', 'booking_date', 'booking_time', 'status', 'created_at')
    search_fields = ('customer__email', 'table__table_number')
    list_filter = ('table', 'booking_date')


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
