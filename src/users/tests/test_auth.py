# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from rest_framework.test import APITestCase
#
# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from drfpasswordless.settings import api_settings, DEFAULTS
# from drfpasswordless.utils import CallbackToken
#
# User = get_user_model()
#
# #TODO переделать тесты
#
#
# class EmailSignUpCallbackTokenTests(APITestCase):
#
#     def setUp(self):
#         api_settings.PASSWORDLESS_EMAIL_NOREPLY_ADDRESS = 'noreply@example.com'
#         self.email_field_name = api_settings.PASSWORDLESS_USER_EMAIL_FIELD_NAME
#
#         self.url = reverse('users:auth_email')
#
#     def test_email_signup_failed(self):
#         email = 'failedemail182+'
#         data = {'email': email}
#
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_email_signup_success(self):
#         email = 'client@example.com'
#         data = {'email': email}
#
#         # Verify user doesn't exist yet
#         user = User.objects.filter(**{self.email_field_name: 'client@example.com'}).first()
#         # Make sure our user isn't None, meaning the user was created.
#         self.assertEqual(user, None)
#
#         # verify a new user was created with serializer
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         user = User.objects.get(**{self.email_field_name: 'client@example.com'})
#         self.assertNotEqual(user, None)
#
#         # Verify a token exists for the user
#         self.assertEqual(CallbackToken.objects.filter(user=user, is_active=True).exists(), 1)
#
#     def test_email_signup_disabled(self):
#         api_settings.PASSWORDLESS_REGISTER_NEW_USERS = False
#
#         # Verify user doesn't exist yet
#         user = User.objects.filter(**{self.email_field_name: 'client@example.com'}).first()
#         # Make sure our user isn't None, meaning the user was created.
#         self.assertEqual(user, None)
#
#         email = 'client@example.com'
#         data = {'email': email}
#
#         # verify a new user was not created
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#         user = User.objects.filter(**{self.email_field_name: 'client@example.com'}).first()
#         self.assertEqual(user, None)
#
#         # Verify no token was created for the user
#         self.assertEqual(CallbackToken.objects.filter(user=user, is_active=True).exists(), 0)
#
#     def tearDown(self):
#         api_settings.PASSWORDLESS_EMAIL_NOREPLY_ADDRESS = DEFAULTS['PASSWORDLESS_EMAIL_NOREPLY_ADDRESS']
#         api_settings.PASSWORDLESS_REGISTER_NEW_USERS = DEFAULTS['PASSWORDLESS_REGISTER_NEW_USERS']
#
#
# class EmailLoginCallbackTokenTests(APITestCase):
#
#     def setUp(self):
#         api_settings.PASSWORDLESS_AUTH_TYPES = ['EMAIL']
#         api_settings.PASSWORDLESS_EMAIL_NOREPLY_ADDRESS = 'noreply@example.com'
#
#         self.email = 'client@example.com'
#         self.url = reverse('users:auth_email')
#         self.challenge_url = reverse('users:auth_token')
#         self.agree = 'True'
#
#         self.email_field_name = api_settings.PASSWORDLESS_USER_EMAIL_FIELD_NAME
#         self.user = User.objects.create(**{self.email_field_name: self.email})
#
#     def test_email_auth_failed(self):
#         data = {'email': self.email}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # Token sent to alias
#         challenge_data = {'email': self.email, 'token': '123456'}  # Send an arbitrary token instead
#
#         # Try to auth with the callback token
#         challenge_response = self.client.post(self.challenge_url, challenge_data)
#         self.assertEqual(challenge_response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_email_auth_missing_alias(self):
#         data = {'email': self.email}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # Token sent to alias
#         callback_token = CallbackToken.objects.filter(user=self.user, is_active=True).first()
#         challenge_data = {'token': callback_token}  # Missing Alias
#
#         # Try to auth with the callback token
#         challenge_response = self.client.post(self.challenge_url, challenge_data)
#         self.assertEqual(challenge_response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_email_auth_bad_alias(self):
#         data = {'email': self.email}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # Token sent to alias. Wrong email.
#         callback_token = CallbackToken.objects.filter(user=self.user, is_active=True).first()
#         challenge_data = {'email': 'abcde@example.com', 'token': callback_token, 'agree': self.agree}  # Bad Alias
#
#         # Second token sent to alias. agree = False
#         second_callback_token = CallbackToken.objects.filter(user=self.user, is_active=True).first()
#         second_challenge_data = {'email': self.email, 'token': second_callback_token, 'agree': 'False'}  # Bad Alias2
#
#
#         # Try to auth with the callback token
#         challenge_response = self.client.post(self.challenge_url, challenge_data)
#         self.assertEqual(challenge_response.status_code, status.HTTP_400_BAD_REQUEST)
#
#         # Try to auth with the callback token 2
#         challenge_response = self.client.post(self.challenge_url, second_challenge_data)
#         self.assertEqual(challenge_response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_email_auth_expired(self):
#         data = {'email': self.email}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # Token sent to alias
#         callback_token = CallbackToken.objects.filter(user=self.user, is_active=True).first()
#         challenge_data = {'email': self.email, 'token': callback_token, 'agree': self.agree}
#
#         data = {'email': self.email}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # Second token sent to alias
#         second_callback_token = CallbackToken.objects.filter(user=self.user, is_active=True).first()
#         second_challenge_data = {'email': self.email, 'token': second_callback_token, 'agree': self.agree}
#
#         # Try to auth with the old callback token
#         challenge_response = self.client.post(self.challenge_url, challenge_data)
#         self.assertEqual(challenge_response.status_code, status.HTTP_400_BAD_REQUEST)
#
#         # Try to auth with the new callback token
#         second_challenge_response = self.client.post(self.challenge_url, second_challenge_data)
#         self.assertEqual(second_challenge_response.status_code, status.HTTP_200_OK)
#
#         # Verify Auth Token
#         auth_token = second_challenge_response.data['token']
#         self.assertEqual(auth_token, Token.objects.filter(key=auth_token).first().key)
#
#     def test_email_auth_success(self):
#         data = {'email': self.email}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # Token sent to alias
#         callback_token = CallbackToken.objects.filter(user=self.user, is_active=True).first()
#         challenge_data = {'email': self.email, 'token': callback_token, 'agree': self.agree}
#
#         # Try to auth with the callback token
#         challenge_response = self.client.post(self.challenge_url, challenge_data)
#         self.assertEqual(challenge_response.status_code, status.HTTP_200_OK)
#
#         # Verify Auth Token
#         auth_token = challenge_response.data['token']
#         self.assertEqual(auth_token, Token.objects.filter(key=auth_token).first().key)
#
#     def tearDown(self):
#         api_settings.PASSWORDLESS_AUTH_TYPES = DEFAULTS['PASSWORDLESS_AUTH_TYPES']
#         api_settings.PASSWORDLESS_EMAIL_NOREPLY_ADDRESS = DEFAULTS['PASSWORDLESS_EMAIL_NOREPLY_ADDRESS']
#         self.user.delete()