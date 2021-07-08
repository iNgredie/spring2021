from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema

from src.users.mixins import MultiSerializerViewSetMixin
from .models import DynamicSettings
from .serializers import (
    DynamicSettingsSerializer,
    DynamicSettingsUpdateSerializer
)
from .permissions import IsSuperUser


@extend_schema_view(
    update=extend_schema(description='Полное обновление динамической настройки'),
    partial_update=extend_schema(description='Частичное обновление динамической настройки'),
    list=extend_schema(description='Получение списка динамических настроек'),
)
class DynamicSettingsViewSet(MultiSerializerViewSetMixin, UpdateModelMixin,
                             ListModelMixin, GenericViewSet):
    """
    Чтение и установка динамических настроек
    """

    queryset = DynamicSettings.objects.all()
    permission_classes = [IsSuperUser]
    serializer_class = DynamicSettingsUpdateSerializer
    serializer_action_classes = {
        'list': DynamicSettingsSerializer,
    }
