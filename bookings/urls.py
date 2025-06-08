from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.public_booking_view, name='public_booking'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('about/', views.about_view, name='about'),
    path('menu/', views.menu_view, name='menu'),
    path('contact/', views.contact_view, name='contact'),
    path('cancel/', views.cancel_booking_view, name='cancel_booking'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
