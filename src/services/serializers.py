from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer

from src.services.models import Service, PriceList
from src.users.mixins import SerializerUserAddressMixin
from src.users.serializers import UserAddressSerializer
from src.users.validators import phone_regex


class ServiceSerializer(SerializerUserAddressMixin, ModelSerializer):
    """
    Сериализатор услуг
    """
    address = UserAddressSerializer()
    phone = CharField(validators=[phone_regex], max_length=16)

    class Meta:
        model = Service
        fields = (
            'id',
            'text',
            'surname',
            'name',
            'patronymic',
            'phone',
            'email',
            'created_at',
            'user',
            'address',
        )
        read_only_fields = ('user',)


class PriceListSerializer(ModelSerializer):
    """
    Сериализатор прайс листов
    """
    price = IntegerField(min_value=0)

    class Meta:
        model = PriceList
        fields = ('id', 'name', 'price')
