from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .filters import TasksFilter
from .models import Task, User
from .permissions import TaskPermissions
from .serializers import TaskSerializer, UserSerializer


class UserCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('status', 'completion_date', )
    filterset_class = TasksFilter

    pagination_class = PageNumberPagination
    page_size = 10
    permission_classes = [IsAuthenticated & TaskPermissions]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
