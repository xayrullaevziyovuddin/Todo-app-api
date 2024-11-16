from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random
from django.core.mail import send_mail


class CustomUser(AbstractUser):
    # OTP для сброса пароля
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_expires = models.DateTimeField(blank=True, null=True)

    # OTP для подтверждения email
    email_otp_code = models.CharField(max_length=6, blank=True, null=True)
    email_otp_expires = models.DateTimeField(blank=True, null=True)

    def generate_email_otp(self):
        """Генерирует OTP для подтверждения email."""
        self.email_otp_code = str(random.randint(100000, 999999))
        self.email_otp_expires = timezone.now() + timezone.timedelta(minutes=5)
        self.save()
        self.send_email_otp()

    def send_email_otp(self):
        """Отправляет OTP для подтверждения email."""
        subject = "Подтверждение вашего email"
        message = f"Ваш OTP код для подтверждения email: {self.email_otp_code}"
        from_email = 'example@example.com'
        recipient_list = [self.email]
        send_mail(subject, message, from_email, recipient_list)

    def is_email_otp_valid(self, otp):
        """Проверяет, является ли OTP для email действительным."""
        return self.email_otp_code == otp and timezone.now() < self.email_otp_expires

