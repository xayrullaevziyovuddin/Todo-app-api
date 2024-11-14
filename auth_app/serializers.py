from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from auth_app.models import CustomUser

User = get_user_model()


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


# Подтверждение OTP и регистрация пользователя
class RegisterWithOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        # Проверяем email и OTP в сессии
        if self.context['request'].session.get('email_for_otp') != email:
            raise serializers.ValidationError("Email не соответствует отправленному OTP.")
        if self.context['request'].session.get('otp_code') != otp:
            raise serializers.ValidationError("Неправильный OTP код.")

        # Проверка срока действия OTP
        otp_expires = self.context['request'].session.get('otp_expires')
        if not otp_expires or timezone.now() > timezone.datetime.fromisoformat(otp_expires):
            raise serializers.ValidationError("Срок действия OTP истек.")
        return data

    def create(self, validated_data):
        # Создание пользователя
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Очистка сессии
        self.context['request'].session.pop('otp_code', None)
        self.context['request'].session.pop('otp_expires', None)
        self.context['request'].session.pop('email_for_otp', None)

        return user


# Отправка OTP на email
class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Проверяем, не существует ли пользователь с таким email
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value
