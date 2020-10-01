from django_filters import rest_framework as filters

from .models import Task


class TasksFilter(filters.FilterSet):
    '''Фильтр для поиска задач с датой выполнения в заданом диапазоне'''

    date_from = filters.DateTimeFilter(
        field_name="completion_date", lookup_expr='gte')
    date_to = filters.DateTimeFilter(
        field_name="completion_date", lookup_expr='lte')

    class Meta:
        model = Task
        fields = ('status', 'date_from', 'date_to', )
