from django.conf import settings
from django.core.mail import send_mail

def email_user(user, token):
    # Send a confirmation email to the user
    subject = "Welcome to Yamak"
    message = "Thank you for registering on Your Site. Please click the link below to confirm your email address:\n\n"
    message += (
        f"{settings.BASE_LOCAL_URL}/api/v1/access/verify-email/{user.uuid}/{token}/"  # Replace with your confirmation URL
    )

    from_email = settings.EMAIL_HOST_USER_EMAIL  # Use the configured email address
    recipient_list = ["abhaykesharwani40@gmail.com"]

    return send_mail(subject, message, from_email, recipient_list, fail_silently=False) 