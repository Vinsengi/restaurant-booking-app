from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.public_booking_view, name='public_booking'),
    path('booking-success/', views.booking_success, name='booking_success'),

]
