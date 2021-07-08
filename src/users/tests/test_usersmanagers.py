from django.test import TestCase
from django.contrib.auth import get_user_model


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(mobile='79876543210', password='paswordtest')
        self.assertEqual(user.mobile, '79876543210')
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(mobile='')
        with self.assertRaises(ValueError):
            User.objects.create_user(mobile='', password="paswordtest")
