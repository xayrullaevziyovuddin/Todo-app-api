from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random
from django.core.mail import send_mail


class CustomUser(AbstractUser):
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_expires = models.DateTimeField(blank=True, null=True)

    def generate_otp(self):
        """Генерирует случайный 6-значный OTP и устанавливает срок его действия."""
        self.otp_code = str(random.randint(100000, 999999))
        self.otp_expires = timezone.now() + timezone.timedelta(minutes=5)  # Устанавливаем срок действия на 5 минут
        self.save()
        self.send_otp_via_email()

    def send_otp_via_email(self):
        """Отправляет OTP на email пользователя."""
        subject = 'Ваш OTP код для сброса пароля'
        message = f'Ваш OTP код: {self.otp_code}'
        from_email = 'example@example.com'  # Измените на реальный email
        recipient_list = [self.email]

        send_mail(subject, message, from_email, recipient_list)

    def is_otp_valid(self, otp):
        """Проверяет, является ли введенный OTP действительным."""
        return self.otp_code == otp and timezone.now() < self.otp_expires

