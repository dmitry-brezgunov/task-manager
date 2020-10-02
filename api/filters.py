from django_filters import rest_framework as filters

from .models import Task


class TasksFilter(filters.FilterSet):
    '''Фильтр для поиска задач с датой выполнения в заданом диапазоне'''

    date_from = filters.DateTimeFilter(
        field_name="completion_date", lookup_expr='gte',
        input_formats=['%d-%m-%Y %H:%M', '%d-%m-%Y'])

    date_to = filters.DateTimeFilter(
        field_name="completion_date", lookup_expr='lte',
        input_formats=['%d-%m-%Y %H:%M', '%d-%m-%Y'])

    class Meta:
        model = Task
        fields = ('status', 'date_from', 'date_to', )
