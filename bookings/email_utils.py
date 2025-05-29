# bookings/utils.py
import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

logger = logging.getLogger(__name__)


def send_booking_email(booking, customer):
    subject = 'Booking Confirmation'
    message = render_to_string('emails/booking_confirmation.html', {
        'booking': booking,
        'customer': customer
    })
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [customer.email],
        fail_silently=False,
        html_message=message
    )
    logger.info(f"Confirmation email sent to {customer.email}")
