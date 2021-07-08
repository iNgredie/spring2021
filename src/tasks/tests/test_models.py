from django.test import TestCase
from django.contrib.auth import get_user_model
from src.users.models import UserAddress
from ..models import Task


User = get_user_model()


class ModelsTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            mobile='89876543210',
            email='user@example.com',
            surname='test Surname',
            name='test Name',
            patronymic='test Patronymic',
        )
        user_address = UserAddress.objects.create(
            street='Lenina',
            house='1',
            building='1',
            apartment='1',
            user=user,
        )
        self.task = Task.objects.create(
            subject='test subject',
            text='test text',
            surname='test Surname',
            name='test Name',
            patronymic='test Patronymic',
            phone='89876543210',
            email='user@example.com',
            user=user,
            address=user_address,
        )

    def test_task_set_completed_at(self):
        '''
        Проверка заполнения поля completed_at при присвоении статуса complete
        '''
        self.task.status = 'complete'
        self.task.save()

        self.assertIsNotNone(self.task.completed_at)
