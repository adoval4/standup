# django
from django.urls import reverse
from django.forms.models import model_to_dict

# Utilities
from nose.tools import ok_, eq_
from faker import Faker

# django rest
from rest_framework import status

# models
from standup.teams.models import Team, Member

# factories
from standup.teams.test.factories import TeamFactory
from standup.users.test.factories import UserFactory

# test utils
from standup.utils.tests import CustomAPITestCase

fake = Faker()


class TestTeamListTestCase(CustomAPITestCase):
	"""
	Tests /users  operations.
	"""

	def setUp(self):
		super().setUp()

		self.url = reverse('team-list')
		self.new_team_data = {
			"name": "new team"
		}
		self.old_team = TeamFactory(
			name="old team",
			created_by=self.user
		)
		self.old_team.managers.add(self.user)

		self.archived_team = TeamFactory(
			name="archived team",
			created_by=self.user,
			is_archived=True
		)
		self.archived_team.managers.add(self.user)

	def test_post_request_with_no_data_fails(self):
		response = self.client.post(self.url, {}, **self.auth_header)
		eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_post_request_without_auth_fails(self):
		response = self.client.post(
			self.url,
			self.new_team_data
		)
		eq_(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_post_request_with_valid_data_succeeds(self):
		response = self.client.post(
			self.url,
			self.new_team_data,
			**self.auth_header
		)
		eq_(response.status_code, status.HTTP_201_CREATED)

		team = Team.objects.get(pk=response.data.get('id'))
		eq_(team.name, self.new_team_data.get('name'))
		eq_(team.created_by.email, self.user.email)
		ok_(team.managers.filter(pk=self.user.pk).exists())

	def test_post_request_with_repeated_name_fails(self):
		response = self.client.post(
			self.url,
			{
				"name": self.old_team.name
			},
			**self.auth_header
		)
		eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_get_request_succeds_when_user_authenticated(self):
		response = self.client.get(
			self.url,
			self.new_team_data,
			**self.auth_header
		)
		eq_(response.status_code, status.HTTP_200_OK)
		eq_(
			response.data.get('count'),
			self.user.managed_teams.filter(is_archived=False).count()
		)

		old_team_found = False
		for team_data in response.data.get('results'):
			if team_data.get('id') == self.old_team.id:
				old_team_found = True
			if team_data.get('id') == self.archived_team.id:
				ok_(False)
		ok_(old_team_found)


class TestTeamDetailsTestCase(CustomAPITestCase):
	"""
	Tests /users/<id> operations.
	"""

	def setUp(self):
		super().setUp()

		self.team = TeamFactory(
			name="the team",
			created_by=self.user
		)
		self.team.managers.add(self.user)
		self.url = reverse('team-detail', kwargs={'pk': self.team.id})

	def test_put_request_valid_data_succeeds(self):
		updated_team_data = {
			"name": "the team 2"
		}
		response = self.client.put(
			self.url,
			updated_team_data,
			**self.auth_header
		)
		eq_(response.status_code, status.HTTP_200_OK)
		team = Team.objects.get(pk=self.team.pk)
		eq_(response.data.get('name'), updated_team_data.get('name'))

	def test_destroy_request_succeeds(self):
		response = self.client.delete(
			self.url,
			**self.auth_header
		)
		eq_(response.status_code, status.HTTP_204_NO_CONTENT)
		team = Team.objects.get(pk=self.team.pk)
		eq_(team.is_archived, True)


class TestTeamMemberListTestCase(CustomAPITestCase):
	"""
	Tests /teams/<id>/members  operations.
	"""

	def setUp(self):
		super().setUp()

		self.team = TeamFactory(
			name="my team",
			created_by=self.user
		)
		self.team.managers.add(self.user)

		self.not_my_team = TeamFactory(
			name="other's team",
		)

		self.team_url = reverse('team_member-list', kwargs={
			'team_id': self.team.id
		})

		self.not_my_team_url = reverse('team_member-list', kwargs={
			'team_id': self.not_my_team.id
		})

		self.new_member_data = {
			'name': fake.first_name(),
			'email': fake.email()
		}

		self.member = Member.objects.create(
			name=fake.first_name(),
			email=fake.email(),
			team=self.team
		)
		self.team_member_url = reverse('team_member-detail', kwargs={
			'team_id': self.team.id,
			'pk': self.member.id,
		})

	def test_post_request_with_no_data_fails(self):
		response = self.client.post(self.team_url, {}, **self.auth_header)
		eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_post_request_without_auth_fails(self):
		response = self.client.post(
			self.team_url, self.new_member_data
		)
		eq_(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_post_request_to_not_my_team_fails(self):
		response = self.client.post(
			self.not_my_team_url, self.new_member_data, **self.auth_header
		)
		eq_(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_post_request_with_valid_data_succeeds(self):
		response = self.client.post(
			self.team_url, self.new_member_data, **self.auth_header
		)
		eq_(response.status_code, status.HTTP_201_CREATED)

		member = Member.objects.get(pk=response.data.get('id'))
		eq_(member.name, self.new_member_data.get('name'))
		eq_(member.created_by.email, self.user.email)
		eq_(member.team.name, self.team.name)

	def test_post_request_with_valid_data_succeeds(self):
		response = self.client.delete(
			self.team_member_url, **self.auth_header
		)
		eq_(response.status_code, status.HTTP_204_NO_CONTENT)
		member = Member.objects.get(pk=self.member.pk)
		eq_(member.is_archived, True)

