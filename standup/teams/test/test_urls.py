# django
from django.test import TestCase
from django.urls import resolve


class TestUrls(TestCase):

	def test_teams_list_url(self):
		path = '/api/v1/teams/'
		assert resolve(path).view_name == 'team-list'

	def test_teams_detail_url(self):
		path = '/api/v1/teams/{}/'.format(
			'1eqsd12e32'
		)
		assert resolve(path).view_name == 'team-detail'

	def test_teams_members_list_url(self):
		path = '/api/v1/teams/{}/members/'.format(
			1
		)
		assert resolve(path).view_name == 'team_member-list'

	def test_teams_members_detail_url(self):
		path = '/api/v1/teams/{}/members/{}/'.format(
			1,
			'1233453456456a'
		)
		assert resolve(path).view_name == 'team_member-detail'