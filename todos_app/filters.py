import django_filters
from .models import Todo


class TodoFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Todo.STATUS_CHOICES)

    class Meta:
        model = Todo
        fields = ['title', 'status']
