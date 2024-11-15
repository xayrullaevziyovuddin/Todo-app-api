from rest_framework import serializers
from .models import Todo


def validate_title(value):
    if Todo.objects.filter(title=value).exists():
        raise serializers.ValidationError("Задача с таким заголовком уже существует.")
    return value


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'status', 'due_date', 'created_date', 'is_special_day']
        read_only_fields = ['user']  # Делаем поле "user" только для чтения