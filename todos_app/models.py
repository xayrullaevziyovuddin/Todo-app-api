from django.db import models

class Todo(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    due_date = models.DateField(null=True, blank=True)  # Поле для дедлайна
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')  # Поле для приоритета

    def __str__(self):
        return self.title
