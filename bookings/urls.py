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
    path('cancel-success/', views.cancel_success_view, name='cancel_success'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    # path('booking/<int:pk>/feedback/', views.leave_feedback, name='leave_feedback'),
    # path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
