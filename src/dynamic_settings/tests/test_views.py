from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import DynamicSettings
from ..serializers import DynamicSettingsSerializer


User = get_user_model()


class TaskTests(APITestCase):

    def setUp(self):
        self.url = reverse('dynamicsettings-list')

        self.superuser = User.objects.create_superuser(
            mobile='+79876543210',
            password='test_password',
        )

        self.non_superuser = User.objects.create_user(
            mobile='+77766655544',
            password='test_password',
        )

        self.dynamic_settings_1 = DynamicSettings.objects.create(
            name='Test name',
            value='Test value',
            description='Test description',
        )

        self.url_detail = reverse('dynamicsettings-detail', args=[self.dynamic_settings_1.id])

        self.client.force_authenticate(user=self.superuser)

    def test_retrieve_settings(self):
        settings = DynamicSettings.objects.all()
        serializer = DynamicSettingsSerializer(settings, many=True)
        response = self.client.get(self.url)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_settings_with_protected_param_by_su(self):
        data = {
            "name": "another name",
            "value": "another value",
            "description": "another decription"
        }

        response = self.client.patch(self.url_detail, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.dynamic_settings_1.refresh_from_db()

        self.assertNotEqual(self.dynamic_settings_1.name, data['name'])
        self.assertEqual(self.dynamic_settings_1.value, data['value'])
        self.assertEqual(self.dynamic_settings_1.description, data['description'])

    def test_update_tasks_by_non_su(self):
        data = {
            "description": "yet another decription"
        }

        self.client.force_authenticate(user=self.non_superuser)

        response = self.client.patch(self.url_detail, data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
