from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Article


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
        self.article = Article.objects.create(
            title='test subject',
            content='test text',
            author=user
        )
