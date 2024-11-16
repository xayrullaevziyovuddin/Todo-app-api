from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from django.contrib.auth import get_user_model
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer, \
    RegisterWithOTPSerializer, SendOTPSerializer
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
import random

User = get_user_model()


# Отправка OTP на email
class SendOTPView(APIView):
    serializer_class = SendOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Генерация OTP
        otp_code = str(random.randint(100000, 999999))
        otp_expires = timezone.now() + timezone.timedelta(minutes=5)

        # Отправка OTP на email
        send_mail(
            subject='Ваш OTP код для подтверждения email',
            message=f'Ваш OTP код: {otp_code}. Он действителен в течение 5 минут.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email]
        )

        # Сохранение данных регистрации и OTP в сессии
        request.session['otp_code'] = otp_code
        request.session['otp_expires'] = otp_expires.isoformat()
        request.session['email_for_otp'] = email
        request.session['username_for_otp'] = username
        request.session['password_for_otp'] = password

        return Response({"message": "OTP был отправлен на ваш email."}, status=status.HTTP_200_OK)


# Подтверждение OTP и регистрация
class RegisterWithOTPView(generics.CreateAPIView):
    serializer_class = RegisterWithOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Регистрация успешно завершена."}, status=status.HTTP_201_CREATED)


# Запрос на сброс пароля (отправка OTP на email)
class PasswordResetRequestView(APIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # Находим пользователя по email
        try:
            user = CustomUser.objects.get(email=email)  # Обновите здесь на вашу модель
        except CustomUser.DoesNotExist:
            return Response({"error": "Пользователь с таким email не найден."}, status=status.HTTP_404_NOT_FOUND)

        # Генерация OTP
        user.generate_otp()
        return Response({"message": "OTP был отправлен на ваш email."}, status=status.HTTP_200_OK)


# Подтверждение OTP и сброс пароля
class PasswordResetConfirmView(APIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Сохранение нового пароля
        serializer.save()

        return Response({"message": "Пароль успешно изменен."}, status=status.HTTP_200_OK)
