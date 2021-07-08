from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Article
from ..serializers import ArticlePreviewSerializer


User = get_user_model()


class TaskTests(APITestCase):

    def setUp(self):
        self.url = reverse('article-list')

        self.user_1 = User.objects.create_user(
            mobile='+79876543210',
            password='test_password',
        )

        # По умолчанию пользователь при создании попадает в группу "Жильцы",
        # нам же нужен пользователь из группы "Сотрудники ТСЖ"
        self.user_1.groups.clear()
        tszh_group = Group.objects.get(name='Сотрудники ТСЖ')
        self.user_1.groups.add(tszh_group)

        self.article_1 = Article.objects.create(
            title='First title',
            content='First text',
            author=self.user_1,
        )

        self.article_2 = Article.objects.create(
            title='Second title',
            content='Second text',
            author=self.user_1,
        )

        self.url_detail = reverse('article-detail', args=[self.article_2.id])

        self.client.force_authenticate(user=self.user_1)

    def test_retrieve_articles(self):
        articles = Article.objects.order_by('-created_at')
        serializer = ArticlePreviewSerializer(articles, many=True)
        response = self.client.get(self.url)

        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_articles(self):
        data = {
            "title": "Third title",
            "content": "Third text",
        }

        response = self.client.post(
            self.url,
            data=data,
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Article.objects.count())
        self.assertEqual(self.user_1, Article.objects.last().author)

    def test_update_articles(self):
        data = {
            "title": "Third title updated",
            "content": "99",
        }

        response = self.client.patch(self.url_detail, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.article_2.refresh_from_db()

        self.assertEqual(self.article_2.title, data['title'])
        self.assertEqual(self.article_2.content, data['content'])
