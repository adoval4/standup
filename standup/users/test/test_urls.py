# django
from django.test import TestCase
from django.urls import resolve


class TestUrls(TestCase):

	def test_users_list_url(self):
		path = '/api/v1/users/'
		assert resolve(path).view_name == 'user-list'

	def test_users_list_url(self):
		path = '/api/v1/users/me/'
		assert resolve(path).view_name == 'user-me'

	def test_users_detail_url(self):
		path = '/api/v1/users/{}/'.format(
			'1eqsd12e32'
		)
		assert resolve(path).view_name == 'user-detail'