import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

logger = logging.getLogger(__name__)


def send_booking_email(booking, customer):
    subject = 'Booking Confirmation'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = customer.email

    context = {
        'booking': booking,
        'customer': customer
    }

    # Render both plain text and HTML
    text_content = render_to_string('emails/booking_confirmation.txt', context)
    html_content = render_to_string('emails/booking_confirmation.html', context)

    # Create the email
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
        logger.info(f"Confirmation email sent to {to_email}")
    except Exception as e:
        logger.exception(f"Failed to send booking confirmation to {to_email}")
        raise e
