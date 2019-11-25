# django
from django.test import TestCase
from django.urls import resolve


class TestUrls(TestCase):

	def test_goals_list_url(self):
		path = '/api/v1/goals/'
		assert resolve(path).view_name == 'goal-list'

	def test_goals_detail_url(self):
		path = '/api/v1/goals/{}/'.format(
			'1eqsd12e32'
		)
		assert resolve(path).view_name == 'goal-detail'
