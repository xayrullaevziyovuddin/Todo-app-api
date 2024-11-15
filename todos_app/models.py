
from django.db import models
from django.utils import timezone
from django.conf import settings


class Todo(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='todos')

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    due_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)  # Поле для даты создания
    is_special_day = models.BooleanField(default=False)  # Булевое поле для особого дня

    def __str__(self):
        return self.title
