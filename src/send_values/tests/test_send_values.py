import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import (
    ValueWaterGasElectricalMeters,
    WaterGasElectricalMeters,
    MetersType
)
from ..serializers import ValuesSerializer

User = get_user_model()


def sample_values(title, user, meter, value):
    """
    Create and return a sample values
    """
    v = ValueWaterGasElectricalMeters.objects.create(
        title=title,
        user=user,
        meter=meter,
        value=value
    )
    return v


class ProfileApiTests(TestCase):
    """Test authenticated API access"""

    def setUp(self):
        self.mobile = '+79876543210'
        self.user = get_user_model().objects.create_user(
            email='example@mail.ru',
            mobile=self.mobile,
            password='passwordtest'
        )
        self.meters_type_gas = MetersType.objects.get(title='Газ')
        self.meters_type_cold_water = MetersType.objects.get(title='Холодная вода')
        self.meter_1 = WaterGasElectricalMeters.objects.create(
            title='gas',
            meters_type=self.meters_type_gas,
            user=self.user
        )
        self.meter_2 = WaterGasElectricalMeters.objects.create(
            title='water',
            meters_type=self.meters_type_cold_water,
            user=self.user
        )
        self.values_meter_1 = ValueWaterGasElectricalMeters.objects.create(
            user=self.user,
            meter=self.meter_1,
            value=1234
        )
        self.values_meter_2 = ValueWaterGasElectricalMeters.objects.create(
            user=self.user,
            meter=self.meter_2,
            value=1500
        )
        self.url = reverse('send_values:values-list')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_values(self):
        values = ValueWaterGasElectricalMeters.objects.all().order_by('id')

        serializer_data = ValuesSerializer(values, many=True).data

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_create_values(self):
        data = {
            "user": self.user.mobile,
            "meter": self.meter_1.id,
            "value": 1234
        }
        json_data = json.dumps(data)
        response = self.client.post(
            self.url,
            data=json_data,
            content_type='application/json'
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, ValueWaterGasElectricalMeters.objects.all().count())
        self.assertEqual(self.user, ValueWaterGasElectricalMeters.objects.last().user)

    def test_update_values(self):
        data = {
            "user": self.user.mobile,
            "meter": self.meter_2.id,
            "value": 2000
        }
        json_data = json.dumps(data)
        url = reverse('send_values:values-detail', args=[self.values_meter_2.id])
        response = self.client.patch(
            url,
            data=json_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.values_meter_2.refresh_from_db()

        self.assertEqual(self.values_meter_2.value, data['value'])

    def test_update_values_not_owner(self):
        self.user2 = User.objects.create(mobile='79822222222')
        data = {
            "user": self.user.mobile,
            "meter": self.meter_2.id,
            "value": 2000
        }
        json_data = json.dumps(data)
        url = reverse('send_values:values-detail', args=[self.values_meter_2.id])
        self.client.force_authenticate(self.user2)
        response = self.client.patch(
            url,
            data=json_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
