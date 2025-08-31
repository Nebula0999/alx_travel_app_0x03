from celery import shared_task
from django.core.mail import send_mail
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')

app = Celery('alx_travel_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@shared_task
def send_payment_confirmation(email, booking_ref):
    send_mail(
        "Payment Confirmation",
        f"Your booking {booking_ref} has been successfully paid.",
        "noreply@travelapp.com",
        [email],
        fail_silently=False,
    )
