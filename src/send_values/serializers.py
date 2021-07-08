from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    IntegerField,
    CharField
)

from .models import (
    ValueWaterGasElectricalMeters,
    WaterGasElectricalMeters,
    MetersType
)
from src.users.serializers import UserAddressSerializer
from src.users.mixins import SerializerUserAddressMixin


class SerializerWaterGasElectricalMeters(SerializerUserAddressMixin, ModelSerializer):
    """
    Сериализатор домовых счетчиков. Адрес берет из UserAddress,
    если его нет создает сам.
    """
    user = CharField(source='user.mobile', read_only=True)
    address = UserAddressSerializer(required=False)
    previous_value = IntegerField(read_only=True)

    class Meta:
        model = WaterGasElectricalMeters
        fields = ('id', 'title', 'user', 'meters_type', 'previous_value', 'address')
        read_only_fields = ('previous_value', )


class ValuesSerializer(ModelSerializer):
    """
    Сериализатор показаний счетчиков.
    """

    user = CharField(source='user.mobile', read_only=True)
    value = IntegerField(min_value=0)
    previous_value = IntegerField(read_only=True)

    def validate(self, data):
        previous_value = data['meter'].previous_value
        if previous_value and previous_value > data['value']:
            raise ValidationError(
                {'value': 'Подаваемое показание должно быть не менее предыдущего.'}
            )
        return super().validate(data)

    class Meta:
        model = ValueWaterGasElectricalMeters
        fields = ('id', 'meter', 'value', 'previous_value', 'user', 'date')
        read_only_fields = ('previous_value', )


class MetersTypeSerializer(ModelSerializer):
    """
    Сериализатор типов счетчиков.
    """

    class Meta:
        model = MetersType
        fields = ('id', 'title', 'measure')
