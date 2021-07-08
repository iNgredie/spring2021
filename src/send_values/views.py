from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import (
    ValueWaterGasElectricalMeters,
    WaterGasElectricalMeters,
    MetersType
)
from .serializers import (
    ValuesSerializer,
    SerializerWaterGasElectricalMeters,
    MetersTypeSerializer
)
from src.users.mixins import OwnerPermMixin


@extend_schema_view(
    create=extend_schema(description='Создание счетчика'),
    retrieve=extend_schema(description='Получение счетчика'),
    update=extend_schema(description='Полное обновление счетчика'),
    partial_update=extend_schema(description='Частичное обновление счетчика'),
    destroy=extend_schema(description='Удаление счетчика'),
    list=extend_schema(description='Получение списка счетчиков'),
)
class WaterGasElectricalMetersViewSet(OwnerPermMixin, ModelViewSet):
    """
    CRUD water/gas/electrical meters
    """
    queryset = WaterGasElectricalMeters.objects.all()
    serializer_class = SerializerWaterGasElectricalMeters
    permission_classes = (DjangoModelPermissions,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    create=extend_schema(description='Создание показания счетчика'),
    retrieve=extend_schema(description='Получение показания счетчика'),
    update=extend_schema(description='Полное обновление показания счетчика'),
    partial_update=extend_schema(description='Частичное обновление показания счетчика'),
    destroy=extend_schema(description='Удаление показания счетчика'),
    list=extend_schema(description='Получение списка показаний счетчиков'),
)
class ValuesViewSet(OwnerPermMixin, ModelViewSet):
    """
    CRUD values meter. And history.
    """
    queryset = ValueWaterGasElectricalMeters.objects.all()
    serializer_class = ValuesSerializer
    permission_classes = (DjangoModelPermissions,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    create=extend_schema(description='Создание типа счетчика'),
    retrieve=extend_schema(description='Получение типа счетчика'),
    update=extend_schema(description='Полное обновление типа счетчика'),
    partial_update=extend_schema(description='Частичное обновление типа счетчика'),
    destroy=extend_schema(description='Удаление типа счетчика'),
    list=extend_schema(description='Получение списка типов счетчиков'),
)
class MetersTypeViewSet(ModelViewSet):
    """
    CRUD Типы счетчиков.
    """
    queryset = MetersType.objects.all()
    serializer_class = MetersTypeSerializer
    permission_classes = (DjangoModelPermissions,)
