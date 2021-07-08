from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from drfpasswordless.settings import api_settings, DEFAULTS
from drfpasswordless.utils import CallbackToken

User = get_user_model()


class MobileSignUpCallbackTokenTests(APITestCase):

    def setUp(self):
        api_settings.PASSWORDLESS_TEST_SUPPRESSION = True
        api_settings.PASSWORDLESS_AUTH_TYPES = ['MOBILE']
        api_settings.PASSWORDLESS_MOBILE_NOREPLY_NUMBER = '+15550000000'
        self.url = reverse('users:auth_mobile')

        self.mobile_field_name = api_settings.PASSWORDLESS_USER_MOBILE_FIELD_NAME

    def test_mobile_signup_failed(self):
        mobile = 'sidfj98zfd'
        data = {'mobile': mobile}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_mobile_signup_success(self):
        mobile = '+15551234567'
        data = {'mobile': mobile}

        # Verify user doesn't exist yet
        user = User.objects.filter(**{self.mobile_field_name: '+15551234567'}).first()
        # Make sure our user isn't None, meaning the user was created.
        self.assertEqual(user, None)

        # verify a new user was created with serializer
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(**{self.mobile_field_name: '+15551234567'})
        self.assertNotEqual(user, None)

        # Verify a token exists for the user
        self.assertEqual(CallbackToken.objects.filter(user=user, is_active=True).exists(), 1)

    def test_mobile_signup_disabled(self):
        api_settings.PASSWORDLESS_REGISTER_NEW_USERS = False

        # Verify user doesn't exist yet
        user = User.objects.filter(**{self.mobile_field_name: '+15557654321'}).first()
        # Make sure our user isn't None, meaning the user was created.
        self.assertEqual(user, None)

        mobile = '+15557654321'
        data = {'mobile': mobile}

        # verify a new user was not created
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(**{self.mobile_field_name: '+15557654321'}).first()
        self.assertEqual(user, None)

        # Verify no token was created for the user
        self.assertEqual(CallbackToken.objects.filter(user=user, is_active=True).exists(), 0)

    def tearDown(self):
        api_settings.PASSWORDLESS_TEST_SUPPRESSION = DEFAULTS['PASSWORDLESS_TEST_SUPPRESSION']
        api_settings.PASSWORDLESS_AUTH_TYPES = DEFAULTS['PASSWORDLESS_AUTH_TYPES']
        api_settings.PASSWORDLESS_REGISTER_NEW_USERS = DEFAULTS['PASSWORDLESS_REGISTER_NEW_USERS']
        api_settings.PASSWORDLESS_MOBILE_NOREPLY_NUMBER = DEFAULTS['PASSWORDLESS_MOBILE_NOREPLY_NUMBER']


def dummy_token_creator(user):
    token = Token.objects.create(key="dummy", user=user)
    return (token, True)