from django.contrib.auth.models import User
import datetime
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer
from django.core.mail import send_mail
from django.conf import settings
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from allauth.account.utils import send_email_confirmation
from allauth.account.models import EmailAddress
from django.views.decorators.csrf import csrf_exempt


# Use TokenObtainPairView for token generation (login)
login_view = TokenObtainPairView.as_view()

# Use TokenRefreshView for token refresh
custom_token_refresh_view = TokenRefreshView.as_view()

class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user  # Get the authenticated user
        serializer = UserSerializer(user)  # Serialize user data
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # user.is_active = False  # Deactivate the user until email verification
            user.save()

            # Create an EmailAddress object and associate it with the user
            email_address, _ = EmailAddress.objects.get_or_create(user=user, email=user.email)
            email_address.primary=True
            email_address.verified=False
            email_address.save()

            # TODO: Send an email confirmation email to the user

            return Response({'message': 'User registered successfully. Check your email for activation instructions.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def email_user(user):
    # Send a confirmation email to the user
    subject = 'Welcome to Your Site - Email Confirmation'
    message = 'Thank you for registering on Your Site. Please click the link below to confirm your email address:\n\n'
    message += f'http://your-site.com/confirm/{user.id}/'  # Replace with your confirmation URL

    from_email = settings.EMAIL_HOST_USER  # Use the configured email address
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
