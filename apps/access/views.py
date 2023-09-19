from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer
from .models import User
from .utils import email_user
from allauth.account.models import EmailAddress
import secrets


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

            # TODO: Send an email confirmation email to the user
            success_code = email_user(user, hex_token)

            if success_code != 1:
                return Response(
                    {
                        "message": "This email is not valid, please provide valid email"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                user.token = hex_token
                user.save()

            return Response(
                {
                    "message": "User registered successfully. Check your email for activation instructions."
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

