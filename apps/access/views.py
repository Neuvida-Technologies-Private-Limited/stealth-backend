import secrets

from allauth.account.models import EmailAddress
from django.conf import settings
from django.http import Http404
from django.urls import reverse
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User
from .serializers import UserSerializer
from .utils import email_user, google_validate_id_token
from .utils import user_get_or_create, user_record_login

# Use TokenObtainPairView for token generation (login)
class CustomTokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get("email", "")
        username = data.get("username", "")
        password = data.get("password", "")
        user = User.objects.filter(email=email).first()
        if not user:
            user = User.objects.filter(username=username).first()
        if not user:
            return Response("Invalid creadentials", status=status.HTTP_401_UNAUTHORIZED)
        if not user.check_password(password):
            return Response("Invalid passwowrd", status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response("Please verify your account", status=status.HTTP_401_UNAUTHORIZED)

        user_record_login(user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response(
            {
                "access_token": access_token,
                "refresh_token": str(refresh)
            },
            status=status.HTTP_200_OK,
        )

# Use TokenRefreshView for token refresh
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Customize the response format
        data = {
            "access_token": response.data["access"],
        }

        return Response(data)


class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user  # Get the authenticated user
        serializer = UserSerializer(user)  # Serialize user data
        return Response(
            {"data": serializer.data, "status_code": status.HTTP_200_OK},
            status=status.HTTP_200_OK,
        )


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

            url = reverse(
                "verify-email-view", kwargs={"uuid": user.uuid, "token": hex_token}
            )

            # Send an email confirmation email to the user
            subject = "Welcome to Yamak"
            message = "Thank you for registering on Our Site. Please click the link below to confirm your email address:\n\n"
            message += (
                f"{settings.BASE_URL}{url}"  # Replace with your confirmation URL
            )
            success_code = email_user(subject, message)

            if success_code != 1:
                return Response(
                    {"message": "This email is not valid."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                user.token = hex_token
                user.save()

            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": serializer.errors, "status_code": status.HTTP_400_BAD_REQUEST}
        )


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uuid, token):
        user = User.objects.filter(uuid=uuid, token=token).first()
        if not user:
            return Response(
                {"message": "Verification URL is invalid or expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_active:
            return Response(
                {"message": "This email is already verified"}, status=status.HTTP_200_OK
            )

        user.is_active = True
        user.token = ""
        user.save()
        email_address = EmailAddress.objects.get(user=user, email=user.email)
        email_address.verified = True
        email_address.save()
        return Response(
            {"message": "Your email has been verified"}, status=status.HTTP_200_OK
        )


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
        url = reverse(
            "reset-password", kwargs={"uuid": user.uuid, "reset_token": hex_token}
        )
        # Send a password reset link to the user
        subject = "Reset Password"
        message = "Please click the link below to reset your password:\n\n"
        message += (
            f"{settings.BASE_URL}{url}"  # Replace with your confirmation URL
        )
        success_code = email_user(subject, message)
        if success_code != 1:
            return Response(
                {"message": "This email is not valid."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            user.reset_password_token = hex_token
            user.save()

        return Response(
            {"message": "Email sent successfully."},
            status=status.HTTP_201_CREATED,
        )


class ResetPassword(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uuid, reset_password_token):
        user = User.objects.filter(uuid=uuid).first()
        if not user:
            return Response(
                {"message": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if user.reset_password_token != reset_password_token:
            return Response(
                {"message": "Token is not valid."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(
            {"message": "Provide new passowrd"},
            status=status.HTTP_200_OK,
        )

    def post(self, request, uuid, reset_password_token):
        user = User.objects.filter(uuid=uuid).first()
        if not user:
            return Response(
                {"message": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if user.reset_password_token != reset_password_token:
            return Response(
                {"message": "Token is not valid."},
                status=status.HTTP_403_FORBIDDEN,
            )
        password = request.data.get("password", "")
        user.set_password(password)
        user.reset_password_token = ""
        user.save()
        return Response(
            {"message": "Password changed."},
            status=status.HTTP_201_CREATED,
        )


@csrf_exempt
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})

class UserInitApi(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        first_name = serializers.CharField(required=False, default='')
        last_name = serializers.CharField(required=False, default='')

    def post(self, request, *args, **kwargs):
        id_token = request.headers.get('id_token')
        is_valid_token, message = google_validate_id_token(id_token=id_token)
        if not is_valid_token:
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # We use get-or-create logic here for the sake of the example.
        # We don't have a sign-up flow.
        user, _ = user_get_or_create(**serializer.validated_data)

        # Generate tokens for the user (access token and refresh token)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response(
            {
                "message": "User registered successfully.",
                "access_token": access_token,
                "refresh_token": str(refresh)
            },
            status=status.HTTP_201_CREATED,
        )
