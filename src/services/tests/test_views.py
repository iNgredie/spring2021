from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.users.models import UserAddress
from ..models import Service, PriceList
from ..serializers import ServiceSerializer, PriceListSerializer


User = get_user_model()


class ServiceTests(APITestCase):

    def setUp(self):
        self.service_list_url = reverse('service-list')
        self.price_list_url = reverse('pricelist-list')

        self.user_1 = User.objects.create_user(
            mobile='+79876543210',
            password='test_password',
        )

        # По умолчанию пользователь при создании попадает в группу "Жильцы",
        # нам же нужен пользователь из группы "Сотрудники ТСЖ"
        self.user_1.groups.clear()
        tszh_group = Group.objects.get(name='Сотрудники ТСЖ')
        self.user_1.groups.add(tszh_group)

        self.user_1_address = UserAddress.objects.create(
            street='Lenina',
            house='1',
            building='1',
            apartment='1',
            user=self.user_1,
        )

        self.user_2 = User.objects.create_user(
            mobile='+77766655544',
            password='test_password',
        )

        self.price_1 = PriceList.objects.create(
            name='First name',
            price=100,
        )

        self.price_2 = PriceList.objects.create(
            name='Second name',
            price=200,
        )

        self.service_1 = Service.objects.create(
            text='First text',
            surname='Lenin',
            name='Vladimir',
            patronymic='Ilyich',
            phone='+79876543210',
            email='lenin@mausoleum.su',
            user=self.user_1,
            address=self.user_1_address,
        )

        self.service_2 = Service.objects.create(
            text='Second text',
            surname='Lenin',
            name='Vladimir',
            patronymic='Ilyich',
            phone='+79876543210',
            email='lenin@mausoleum.su',
            user=self.user_1,
            address=self.user_1_address,
        )

        self.service_list_url_detail = reverse('service-detail', args=[self.service_2.id])
        self.price_list_url_detail = reverse('pricelist-detail', args=[self.price_2.id])

        self.client.force_authenticate(user=self.user_1)

    def test_retrieve_services(self):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        response = self.client.get(self.service_list_url)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_services(self):
        data = {
            "text": "Third text",
            "surname": "Kerensky",
            "name": "Alexander",
            "patronymic": "Fyodorovich",
            "phone": "+79626320009",
            "email": "kerensky@example.com",

            "address.street": "Goncharova",
            "address.house": "2",
            "address.building": "2",
            "address.apartment": "2"
        }

        response = self.client.post(
            self.service_list_url,
            data=data,
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Service.objects.count())
        self.assertEqual(self.user_1, Service.objects.last().user)

    def test_update_services(self):
        data = {
            "text": "Third text updated",
            "address.house": "99",
        }

        response = self.client.patch(self.service_list_url_detail, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.service_2.refresh_from_db()

        self.assertEqual(self.service_2.text, data['text'])
        self.assertEqual(self.service_2.address.house, data['address.house'])

    def test_retrieve_prices(self):
        prices = PriceList.objects.all()
        serializer = PriceListSerializer(prices, many=True)
        response = self.client.get(self.price_list_url)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_prices(self):
        data = {
            "name": "Third name",
            "price": 300,
        }

        response = self.client.post(
            self.price_list_url,
            data=data,
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, PriceList.objects.count())

    def test_update_prices(self):
        data = {
            "price": 400,
        }

        response = self.client.patch(self.price_list_url_detail, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.price_2.refresh_from_db()

        self.assertEqual(self.price_2.price, data['price'])
