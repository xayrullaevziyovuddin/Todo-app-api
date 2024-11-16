from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import random
from .models import CustomUser
from .serializers import (
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    RegisterWithOTPSerializer,
    SendOTPSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()


# Отправка OTP для регистрации
class SendOTPView(APIView):
    serializer_class = SendOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Генерация OTP для подтверждения email
        otp_code = str(random.randint(100000, 999999))
        otp_expires = timezone.now() + timezone.timedelta(minutes=5)

        try:
            send_mail(
                subject='Ваш OTP код для подтверждения email',
                message=f'Ваш OTP код: {otp_code}. Он действителен в течение 5 минут.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({"error": f"Ошибка отправки email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Сохранение данных временно в сессии
        request.session['otp_code'] = otp_code
        request.session['otp_expires'] = otp_expires.isoformat()
        request.session['email_for_otp'] = email
        request.session['username_for_otp'] = username
        request.session['password_for_otp'] = password

        return Response({"message": "OTP был отправлен на ваш email."}, status=status.HTTP_200_OK)


# Подтверждение OTP и регистрация
class RegisterWithOTPView(APIView):
    serializer_class = RegisterWithOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Получаем данные из сессии
        email = request.session.get('email_for_otp')
        username = request.session.get('username_for_otp')
        password = request.session.get('password_for_otp')

        if not all([email, username, password]):
            return Response({"error": "Данные для создания пользователя отсутствуют."}, status=status.HTTP_400_BAD_REQUEST)

        # Создание пользователя
        user = User.objects.create_user(username=username, email=email, password=password)

        # Очистка сессии
        request.session.flush()

        return Response({"message": "Регистрация успешно завершена."}, status=status.HTTP_201_CREATED)


# Запрос на сброс пароля
class PasswordResetRequestView(APIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # Найдем пользователя по email
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Пользователь с таким email не найден."}, status=status.HTTP_404_NOT_FOUND)

        # Генерация OTP для сброса пароля
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
