from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Todo
from .serializers import TodoSerializer
from .filters import TodoFilter
from rest_framework.permissions import IsAuthenticated


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TodoFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Возвращаем задачи только текущего пользователя
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя как владельца задачи
        serializer.save(user=self.request.user)
