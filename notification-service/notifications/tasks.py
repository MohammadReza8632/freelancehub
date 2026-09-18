from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_notification_email(recipient_email, subject, message):
    send_mail(
        subject,
        message,
        'noreply@freelancehub.com',
        [recipient_email],

    )