from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'status', 'due_date', 'created_date', 'is_special_day']
        read_only_fields = ['user']  # Делаем поле "user" только для чтения

    def validate_title(self, value):
        if Todo.objects.filter(title=value, user=self.context['request'].user).exists():
            raise serializers.ValidationError("Задача с таким заголовком уже существует.")
        return value
