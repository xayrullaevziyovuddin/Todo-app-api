import django_filters
from .models import Todo
from django_filters import rest_framework as filters
from datetime import date, timedelta


class TodoFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Todo.STATUS_CHOICES)
    due_date = filters.DateFromToRangeFilter()

    today = filters.BooleanFilter(method='filter_today', label='Сегодня')
    this_week = filters.BooleanFilter(method='filter_this_week', label='Эта неделя')
    this_month = filters.BooleanFilter(method='filter_this_month', label='Этот месяц')

    class Meta:
        model = Todo
        fields = ['title', 'status', 'due_date', 'today', 'this_week', 'this_month']

    def filter_today(self, queryset, name, value):
        if value:
            return queryset.filter(due_date=date.today())
        return queryset

    def filter_this_week(self, queryset, name, value):
        if value:
            start_of_week = date.today() - timedelta(days=date.today().weekday())
            end_of_week = start_of_week + timedelta(days=6)
            return queryset.filter(due_date__range=(start_of_week, end_of_week))
        return queryset

    def filter_this_month(self, queryset, name, value):
        if value:
            start_of_month = date.today().replace(day=1)
            end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            return queryset.filter(due_date__range=(start_of_month, end_of_month))
        return queryset
