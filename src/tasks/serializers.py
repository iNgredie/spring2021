from rest_framework import serializers
from .models import Task, TaskStatus
from src.users.serializers import UserAddressSerializer
from src.users.mixins import SerializerUserAddressMixin
from src.users.validators import phone_regex


class TaskStatusSerializer(serializers.ModelSerializer):
    """
    Сериализатор для статусов заявок.
    """
    class Meta:
        model = TaskStatus
        fields = ('id', 'title')


class TaskSerializer(SerializerUserAddressMixin, serializers.ModelSerializer):
    """
    Сериализатор для подачи заявок.
    """
    address = UserAddressSerializer()
    phone = serializers.CharField(validators=[phone_regex], max_length=16)

    class Meta:
        model = Task
        fields = (
            'id',
            'subject',
            'text',
            'surname',
            'name',
            'patronymic',
            'phone',
            'email',
            'created_at',
            'completed_at',
            'task_status',
            'user',
            'performer',
            'attachment',
            'address',
        )
        read_only_fields = ('completed_at', 'performer', 'user', 'task_status')
