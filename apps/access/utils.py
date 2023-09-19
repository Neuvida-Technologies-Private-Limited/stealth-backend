from django.conf import settings
from django.core.mail import send_mail

def email_user(subject, message):
    from_email = settings.EMAIL_HOST_USER_EMAIL  # Use the configured email address
    recipient_list = ["abhaykesharwani40@gmail.com"]

    return send_mail(subject, message, from_email, recipient_list, fail_silently=False) 