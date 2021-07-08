from .models import UserAddress


class SerializerUserAddressMixin():
    """
    Mixin для сериализаторов с возможностью сохранить адрес.
    Адрес берет из UserAddress, если его нет создает сам.
    """
    def create(self, validated_data):
        address_data = validated_data.pop('address', None)

        if address_data:
            address, _ = UserAddress.objects.get_or_create(
                user=validated_data['user'],
                **address_data
            )
            validated_data.update({'address': address})

        return super().create(validated_data)

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)

        if address_data:
            is_partial_equal = True
            for k in ('street', 'house', 'building', 'apartment'):
                if instance.address:
                    current_value = getattr(instance.address, k)
                else:
                    current_value = None
                if k in address_data:
                    if address_data[k] != current_value:
                        is_partial_equal = False
                else:
                    address_data[k] = current_value

            if not is_partial_equal:
                address, _ = UserAddress.objects.get_or_create(
                    user=instance.user,
                    **address_data
                )
                validated_data.update({'address': address})

        return super().update(instance, validated_data)


class OwnerPermMixin():
    """
    Mixin для ViewSet с дополнительным разграничением доступа:
    Суперпользователи и Сотрудники ТСЖ - без фильтрации
    Жильцы - только свое
    Остальные - ничего

    owner_field - строка. Название поля по которому определяем владельца.
    """
    owner_field = 'user'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            pass
        else:
            groups = self.request.user.groups.values_list('name', flat=True)
            if 'Сотрудники ТСЖ' in groups:
                pass
            elif 'Жильцы' in groups:
                qs = qs.filter(**{self.owner_field: self.request.user.pk})
            else:
                qs = qs.none()
        return qs


class MultiSerializerViewSetMixin(object):
    """
    https://stackoverflow.com/a/22922156
    """
    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.

        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()
