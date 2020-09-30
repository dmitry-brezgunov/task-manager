from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, UserCreate

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('auth/token/', views.obtain_auth_token),
    path('auth/register/', UserCreate.as_view()),
    path('', include(router.urls))
]