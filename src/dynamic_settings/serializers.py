from rest_framework import serializers
from .models import DynamicSettings


class DynamicSettingsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для справочника
    """
    class Meta:
        model = DynamicSettings
        fields = ('id', 'name', 'value', 'description')


class DynamicSettingsUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор справочника для обновления
    """
    class Meta:
        model = DynamicSettings
        fields = ('value', 'description')
