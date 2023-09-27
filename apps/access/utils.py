import requests
from typing import Tuple

from django.db import transaction
from django.core.management.utils import get_random_secret_key
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.utils import timezone

# from rest_framework_jwt.settings import api_settings
# from rest_framework_jwt.compat import set_cookie_with_token

from .constants import GOOGLE_ID_TOKEN_INFO_URL

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


def google_validate_id_token(*, id_token: str) -> bool:
    response = requests.get(
        GOOGLE_ID_TOKEN_INFO_URL,
        params={'id_token': id_token}
    )
    # print(response.json())
    if not response.ok:
        return False, 'id_token is invalid.'

    audience = response.json()['aud']

    if audience != settings.GOOGLE_OAUTH2_CLIENT_ID:
        return False, 'Invalid audience.'

    return True, 'Token is valid'

def user_create(email, password=None, **extra_fields) -> User:
    extra_fields = {
        'is_staff': False,
        'is_superuser': False,
        **extra_fields
    }

    user = User(email=email, **extra_fields)

    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()

    user.full_clean(exclude=["username"])
    user.save()

    return user


def user_create_superuser(email, password=None, **extra_fields) -> User:
    extra_fields = {
        **extra_fields,
        'is_staff': True,
        'is_superuser': True
    }

    user = user_create(email=email, password=password, **extra_fields)

    return user


def user_record_login(user: User) -> User:
    user.last_login = timezone.now()
    user.save()


@transaction.atomic
def user_change_secret_key(*, user: User) -> User:
    user.secret_key = get_random_secret_key()
    user.full_clean()
    user.save()

    return user


@transaction.atomic
def user_get_or_create(*, email: str, **extra_data) -> Tuple[User, bool]:
    user = User.objects.filter(email=email).first()

    if user:
        return user, False

    return user_create(email=email, **extra_data), True
