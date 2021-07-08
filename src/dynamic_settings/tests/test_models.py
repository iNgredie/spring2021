from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from ..models import DynamicSettings


User = get_user_model()


class ModelsTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            mobile='89876543210',
            password='test psw',
        )
        self.dynamic_settings_1 = DynamicSettings.objects.create(
            name='Test name',
            value='Test value',
            description='Test description',
        )

    def test_unique_name(self):
        '''
        Проверка уникальности поля name
        '''
        settings_2 = DynamicSettings(
            name='Test name',
            value='another Test value',
            description='another Test description',
        )

        with self.assertRaises(Exception) as raised:
            settings_2.save()
        self.assertEqual(IntegrityError, type(raised.exception))
