from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


def email_user(subject, message):
    from_email = settings.EMAIL_HOST_USER_EMAIL  # Use the configured email address
    recipient_list = ["abhaykesharwani40@gmail.com"]

    return send_mail(subject, message, from_email, recipient_list, fail_silently=False)


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if the provided username is an email
            user = User.objects.get(Q(email=username) | Q(username=username))
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
