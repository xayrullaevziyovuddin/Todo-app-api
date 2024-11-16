from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from auth_app.models import CustomUser

User = get_user_model()


# Подтверждение OTP и регистрация пользователя
class RegisterWithOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        # Получение данных из сессии
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError("Контекст запроса отсутствует.")

        session_email = request.session.get('email_for_otp')
        session_otp = request.session.get('otp_code')
        session_expiry = request.session.get('otp_expires')

        if not session_email or session_email != email:
            raise serializers.ValidationError("Email не совпадает с тем, на который был отправлен OTP.")

        if not session_otp or session_otp != otp:
            raise serializers.ValidationError("Неправильный OTP код.")

        if not session_expiry or timezone.now() > timezone.datetime.fromisoformat(session_expiry):
            raise serializers.ValidationError("Срок действия OTP истек.")

        return data


# Отправка OTP на email
class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        # Проверяем, не существует ли пользователь с таким email
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден.")

        # Проверка валидности OTP
        if not user.is_otp_valid(otp):  # Этот метод должен быть в вашей модели User
            raise serializers.ValidationError("Неправильный или истекший OTP код.")

        return data

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']

        user = User.objects.get(email=email)
        user.set_password(new_password)  # Установка нового пароля
        user.otp_code = None  # Очистка OTP
        user.otp_expires = None  # Очистка срока действия OTP
        user.save()

        return user
