from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.public_booking_view, name='public_booking'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('about/', views.about_view, name='about'),
    path('menu/', views.menu_view, name='menu'),
    path('contact/', views.contact_view, name='contact'),
    path('cancel/', views.cancel_booking_view, name='cancel_booking'),



]
