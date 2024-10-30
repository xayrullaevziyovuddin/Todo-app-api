from django.db import models
from django.utils import timezone


class Todo(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    due_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)  # Поле для даты создания
    is_special_day = models.BooleanField(default=False)  # Булевое поле для особого дня

    def __str__(self):
        return self.title
