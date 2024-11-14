from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer

User = get_user_model()


# Для создания пользователя
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


# Запрос на сброс пароля (отправка OTP на email)
# Ваша логика в PasswordResetRequestView остается прежней
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
