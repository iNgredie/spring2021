from django.contrib.auth import get_user_model
# from django.http import response
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.users.models import UserAddress
from ..models import Task
from ..serializers import TaskSerializer


User = get_user_model()


class TaskTests(APITestCase):

    def setUp(self):
        self.url = reverse('task-list')

        self.user_1 = User.objects.create_user(
            mobile='+79876543210',
            password='test_password',
        )

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

        self.task_1 = Task.objects.create(
            subject='First subject',
            text='First text',
            surname='Lenin',
            name='Vladimir',
            patronymic='Ilyich',
            phone='+79876543210',
            email='lenin@mausoleum.su',
            user=self.user_1,
            address=self.user_1_address,
            attachment=None
        )

        self.task_2 = Task.objects.create(
            subject='Second subject',
            text='Second text',
            surname='Lenin',
            name='Vladimir',
            patronymic='Ilyich',
            phone='+79876543210',
            email='lenin@mausoleum.su',
            user=self.user_1,
            address=self.user_1_address,
            attachment=None
        )

        self.url_detail = reverse('task-detail', args=[self.task_2.id])

        self.client.force_authenticate(user=self.user_1)

    def test_retrieve_tasks(self):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        response = self.client.get(self.url)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_tasks(self):
        data = {
            "subject": "Third subject",
            "text": "Third text",
            "surname": "Kerensky",
            "name": "Alexander",
            "patronymic": "Fyodorovich",
            "phone": "+79626320009",
            "email": "kerensky@example.com",
            "attachment": "",

            "address.street": "Goncharova",
            "address.house": "2",
            "address.building": "2",
            "address.apartment": "2"
        }

        response = self.client.post(
            self.url,
            data=data,
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Task.objects.count())
        self.assertEqual(self.user_1, Task.objects.last().user)

    def test_update_tasks(self):
        data = {
            "subject": "Third subject updated",
            "address.house": "99",
        }

        response = self.client.patch(self.url_detail, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.task_2.refresh_from_db()

        self.assertEqual(self.task_2.subject, data['subject'])
        self.assertEqual(self.task_2.address.house, data['address.house'])

    def test_update_tasks_not_owner(self):
        data = {
            "subject": "Third subject updated by user_2",
        }

        self.client.force_authenticate(user=self.user_2)

        response = self.client.patch(self.url_detail, data=data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
