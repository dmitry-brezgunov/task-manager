from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .filters import TasksFilter
from .models import Task, TaskHistory
from .permissions import TaskPermissions
from .serializers import TaskHistorySerializer, TaskSerializer, UserSerializer


class UserCreate(APIView):
    '''View для регистрации пользователей'''

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'success': 'Вы успешно зарегистрированны'},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(ModelViewSet):
    '''ViewSet для создания, изменения, удаления, просмотра списка задач.
    Фильтрация, пагинация. Доступно только пользователям с токеном.
    Возможно просматривать и редактировать только свои задачи'''

    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('status', 'completion_date', )
    filterset_class = TasksFilter

    pagination_class = PageNumberPagination
    page_size = 10
    permission_classes = [IsAuthenticated & TaskPermissions]

    def get_queryset(self):
        '''Вывод списка задач только текущего пользователя'''

        user = self.request.user
        return Task.objects.filter(user=user)

    def perform_create(self, serializer):
        '''Добавление текущего пользователя при создании задачи'''

        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def history(self, request, pk):
        '''Вывод списка с историей изменения задачи'''

        task = get_object_or_404(Task, pk=pk, user=request.user)
        task_history = TaskHistory.objects.filter(task=task)
        page = self.paginate_queryset(task_history)
        serializer = TaskHistorySerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
