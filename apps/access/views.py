import secrets

from allauth.account.models import EmailAddress
from django.conf import settings
from django.http import Http404
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .models import User
from .serializers import UserSerializer
from .utils import email_user

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

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # Deactivate the user until email verification
            user.save()

            # Create an EmailAddress object and associate it with the user
            email_address, _ = EmailAddress.objects.get_or_create(
                user=user, email=user.email
            )
            email_address.primary = True
            email_address.verified = False
            email_address.save()

            # Generating token for email verification
            # Convert the byte token to a hex string
            hex_token = secrets.token_hex(16)

            url = reverse("verify-email-view", kwargs={"uuid": user.uuid, "token": hex_token})

            # Send an email confirmation email to the user
            subject = "Welcome to Yamak"
            message = "Thank you for registering on Your Site. Please click the link below to confirm your email address:\n\n"
            message += (
                f"{settings.BASE_LOCAL_URL}{url}"  # Replace with your confirmation URL
            )
            success_code = email_user(subject, message)

            if success_code != 1:
                return Response(
                    {
                        "message": "This email is not valid."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                user.token = hex_token
                user.save()

            return Response(
                {
                    "message": "User registered successfully."
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uuid, token):
        user = User.objects.filter(uuid=uuid, token=token).first()
        if not user:
            return Response({"message": "Verification URL is invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({"message": "This email is already verified"}, status=status.HTTP_200_OK)

        user.is_active = True
        user.token = ""
        user.save()
        email_address = EmailAddress.objects.get(
            user=user, email=user.email
        )
        email_address.verified = True
        email_address.save()
        return Response({"message": "Your email has been verified"}, status=status.HTTP_200_OK)


class ResetPasswordMail(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "")
        user = None
        try:
            user = User.objects.get(email=email)
        except:
            raise Http404

        hex_token = secrets.token_hex(16)
        url = reverse("reset-password",  kwargs={"uuid": user.uuid, "reset_token": hex_token})
        # Send a password reset link to the user
        subject = "Reset Password"
        message = "Please click the link below to reset your password:\n\n"
        message += (
            f"{settings.BASE_LOCAL_URL}{url}"  # Replace with your confirmation URL
        )
        success_code = email_user(subject, message)
        if success_code != 1:
            return Response(
                {
                    "message": "This email is not valid."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            user.reset_password_token = hex_token
            user.save()

        return Response(
            {
                "message": "Email sent successfully."
            },
            status=status.HTTP_201_CREATED,
        )

class ResetPassword(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uuid, reset_password_token):
        user = User.objects.filter(uuid=uuid).first()
        if not user:
            return Response(
                {
                    "message": "User not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        if user.reset_password_token != reset_password_token:
            return Response(
                {
                    "message": "Token is not valid."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(
            {
                "message": "Provide new passowrd"
            },
            status=status.HTTP_200_OK,
        )
    
    def post(self, request, uuid, reset_password_token):
        user = User.objects.filter(uuid=uuid).first()
        if not user:
            return Response(
                {
                    "message": "User not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        if user.reset_password_token != reset_password_token:
            return Response(
                {
                    "message": "Token is not valid."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        password = request.data.get("password", "")
        user.set_password(password)
        user.reset_password_token = ""
        user.save()
        return Response(
            {
                "message": "Password changed."
            },
            status=status.HTTP_201_CREATED,
        )