from django.contrib.auth import get_user_model
from rest_framework import serializers
from drfpasswordless.serializers import CallbackTokenAuthSerializer
from rest_framework.serializers import ModelSerializer, Serializer
from .models import UserAddress
from .utils import get_token_for_user


User = get_user_model()


class CustomCallbackTokenAuthSerializer(CallbackTokenAuthSerializer):
    """
    Ввод пароля. Соглашение с лицензией. В ответ приходит токен.
    """
    email = None
    agree = serializers.BooleanField()

    def validate_agree(self, value):
        if not value:
            raise serializers.ValidationError('please, accept license agreement')
        return value


class UserAddressSerializer(ModelSerializer):
    """
    Сериализация адреса пользователя
    """
    class Meta:
        model = UserAddress
        fields = ('id', 'street', 'house', 'building', 'apartment', 'user',)
        read_only_fields = ('id', 'user')


class UserAddressIsMainSerializer(ModelSerializer):
    """
    Сериализация адреса пользователя
    с полем is_main
    """
    class Meta:
        model = UserAddress
        fields = ('id', 'street', 'house', 'building', 'apartment', 'user', 'is_main')
        read_only_fields = ('id', 'user')


class UserProfileSerializer(ModelSerializer):
    """
    Сериализация профиля пользователя
    """
    addresses = UserAddressIsMainSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'mobile',
            'email',
            'surname',
            'name',
            'patronymic',
            'personal_account',
            'addresses',
            'attachment'
        )
        read_only_fields = ('mobile', 'addresses')


class UserProfileUpdateSerializer(ModelSerializer):
    """
    Сериализация профиля пользователя.
    Принимает только один Адрес!
    Если адрес не существует, он будет добавлен к списку адресов клиента
    (без удаления старых).
    Адрес будет отмечен как основной (атрибут is_main=True)
    """
    address = UserAddressSerializer(required=False)

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)

        try:
            current_address = instance.addresses.get(is_main=True)
        except UserAddress.DoesNotExist:
            current_address = None

        if address_data:
            is_updated = False

            for k in ('street', 'house', 'building', 'apartment'):
                current_value = getattr(current_address, k, '')
                if k in address_data:
                    if address_data[k] != current_value:
                        is_updated = True
                else:
                    address_data[k] = current_value

            if is_updated:
                try:
                    address = UserAddress.objects.get(
                        user=instance,
                        **address_data
                    )
                    address.is_main = True
                    address.save()
                except UserAddress.DoesNotExist:
                    address = UserAddress.objects.create(
                        user=instance,
                        is_main=True,
                        **address_data
                    )
            else:
                address = current_address
        else:
            address = current_address

        validated_data.update({'address': address})

        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = (
            'mobile',
            'email',
            'surname',
            'name',
            'patronymic',
            'personal_account',
            'address',
            'attachment'
        )
        read_only_fields = ('mobile', )


class JWTAuthTokenSerializer(Serializer):
    """
    Сериализатор, возвращающий JWT токен
    """
    access = serializers.CharField()

    def __init__(self, *args, **kwargs):
        user_id = kwargs['data']['payload']['user_id']
        self.user = User.objects.get(pk=user_id)
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        data = super().validate(attrs)
        token, _ = get_token_for_user(self.user)
        data['access'] = str(token)
        return data
