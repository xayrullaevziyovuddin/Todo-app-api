from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import PasswordResetRequestView, PasswordResetConfirmView, SendOTPView, RegisterWithOTPView

urlpatterns = [
    path('signup/', SendOTPView.as_view(), name='signup'),  # Отправка OTP
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/confirm/', RegisterWithOTPView.as_view(), name='register_with_otp'), # Завершение регистрации по OTP
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # Пути для сброса пароля через OTP
    path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password_reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
