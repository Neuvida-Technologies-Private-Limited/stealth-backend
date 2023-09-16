from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Use TokenObtainPairView for token generation (login)
login_view = TokenObtainPairView.as_view()

# Use TokenRefreshView for token refresh
custom_token_refresh_view = TokenRefreshView.as_view()