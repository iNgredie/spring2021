from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import Task, TaskStatus
from .serializers import TaskSerializer, TaskStatusSerializer
from rest_framework.permissions import DjangoModelPermissions
from src.users.mixins import OwnerPermMixin


@extend_schema_view(
    create=extend_schema(description='Создание заявки'),
    retrieve=extend_schema(description='Получение заявки'),
    update=extend_schema(description='Полное обновление заявки'),
    partial_update=extend_schema(description='Частичное обновление заявки'),
    destroy=extend_schema(description='Удаление заявки'),
    list=extend_schema(description='Получение списка заявок'),
)
class TaskViewSet(OwnerPermMixin, ModelViewSet):
    """
    CRUD для заявок
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (DjangoModelPermissions, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    create=extend_schema(description='Создание статуса заявки'),
    retrieve=extend_schema(description='Получение статуса заявки'),
    update=extend_schema(description='Полное обновление статуса заявки'),
    partial_update=extend_schema(description='Частичное обновление статуса заявки'),
    destroy=extend_schema(description='Удаление статуса заявки'),
    list=extend_schema(description='Получение статусов заявок'),
)
class TaskStatusViewSet(ModelViewSet):
    """
    CRUD для статусов заявок
    """
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSerializer
    permission_classes = (DjangoModelPermissions, )
