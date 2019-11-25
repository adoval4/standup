# django rest
from rest_framework.test import APITestCase

# django rest
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

# factories
from standup.users.test.factories import UserFactory


class CustomAPITestCase(APITestCase):
	"""
	Base user api test case
	"""

	def setUp(self):
		self.user = UserFactory()
		self.user_token = Token.objects.get(user=self.user)
		self.auth_header = user_token_header = {
			'HTTP_AUTHORIZATION': 'Token {}'.format(self.user_token.key)
		}