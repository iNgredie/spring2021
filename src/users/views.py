from django.contrib.auth import get_user_model
from drfpasswordless.views import ObtainAuthTokenFromCallbackToken
from rest_framework import mixins
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import UserAddress
from .serializers import (
    CustomCallbackTokenAuthSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    UserAddressIsMainSerializer
)
from .mixins import OwnerPermMixin, MultiSerializerViewSetMixin


User = get_user_model()


class CustomObtainAuthTokenFromCallbackToken(ObtainAuthTokenFromCallbackToken):
    """
    Ввод пароля. В ответ приходит токен.
    """
    serializer_class = CustomCallbackTokenAuthSerializer


@extend_schema_view(
    retrieve=extend_schema(description='Получение профиля пользователя'),
    update=extend_schema(description='Полное обновление профиля пользователя'),
    partial_update=extend_schema(description='Частичное обновление профиля пользователя'),
    destroy=extend_schema(description='Удаление профиля пользователя'),
    list=extend_schema(description='Получение списка профилей пользователей'),
)
class UserProfileView(MultiSerializerViewSetMixin, OwnerPermMixin,
                      mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin, mixins.ListModelMixin,
                      GenericViewSet):
    """
    Заполнение профиля пользователя
    """
    queryset = User.objects.all()
    permission_classes = (DjangoModelPermissions,)
    owner_field = 'pk'

    serializer_class = UserProfileSerializer
    serializer_action_classes = {
        'update': UserProfileUpdateSerializer,
        'partial_update': UserProfileUpdateSerializer,
    }

    def perform_update(self, serializer):
        serializer.save(mobile=self.request.user.mobile)


@extend_schema_view(
    create=extend_schema(description='Создание адреса пользователя'),
    retrieve=extend_schema(description='Получение адреса пользователя'),
    update=extend_schema(description='Полное обновление адреса пользователя'),
    partial_update=extend_schema(description='Частичное обновление адреса пользователя'),
    destroy=extend_schema(description='Удаление адреса пользователя'),
    list=extend_schema(description='Получение списка адресов пользователей'),
)
class UserAddressView(OwnerPermMixin, ModelViewSet):
    """
    CRUD адреса пользователя
    """
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressIsMainSerializer
    permission_classes = (DjangoModelPermissions,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)