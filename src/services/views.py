from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema

from src.services.models import Service, PriceList
from src.services.serializers import ServiceSerializer, PriceListSerializer


@extend_schema_view(
    create=extend_schema(description='Создание услуги'),
    retrieve=extend_schema(description='Получение услуги'),
    update=extend_schema(description='Полное обновление услуги'),
    partial_update=extend_schema(description='Частичное обновление услуги'),
    destroy=extend_schema(description='Удаление услуги'),
    list=extend_schema(description='Получение списка услуг'),
)
class ServiceView(ModelViewSet):
    """
    CRUD для услуг
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (DjangoModelPermissions,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    create=extend_schema(description='Создание позиции прайс-листа'),
    retrieve=extend_schema(description='Получение позиции прайс-листа'),
    update=extend_schema(description='Полное обновление позиции прайс-листа'),
    partial_update=extend_schema(description='Частичное обновление позиции прайс-листа'),
    destroy=extend_schema(description='Удаление позиции прайс-листа'),
    list=extend_schema(description='Получение полного прайс-листа'),
)
class PriceListView(ModelViewSet):
    """
    CRUD для прайс листов
    """
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer
    permission_classes = (DjangoModelPermissions,)
