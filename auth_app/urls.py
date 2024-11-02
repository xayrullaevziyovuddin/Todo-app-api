from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserCreateView
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', reset_password_request_token, name='password_reset'),
    path('password_reset/confirm/', reset_password_confirm, name='password_reset_confirm'),
]
