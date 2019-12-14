# django
from django.urls import reverse
from django.forms.models import model_to_dict

# Utilities
from nose.tools import ok_, eq_
from faker import Faker

# django rest
from rest_framework import status

# models
from standup.teams.models import Team, Member, TeamSettings
from standup.goals.models import Goal

# factories
from standup.teams.test.factories import TeamFactory, MemberFactory
from standup.users.test.factories import UserFactory
from standup.goals.test.factories import GoalFactory

# test utils
from standup.utils.tests import CustomAPITestCase

fake = Faker()


class TestTeamListTestCase(CustomAPITestCase):
	"""
	Tests /teams/  operations.
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
	Tests /teams/<id>/ operations.
	"""

	def setUp(self):
		super().setUp()

		self.team = TeamFactory(
			name="the team",
			created_by=self.user
		)
		self.team.managers.add(self.user)
		self.url = reverse('team-detail', kwargs={'pk': self.team.id})

		self.member = MemberFactory(team=self.team)
		self.pending_goal_1 = GoalFactory(
			member=self.member,
			created_by=self.user
		)
		self.pending_goal_2 = GoalFactory(
			member=self.member,
			created_by=self.user,
			status=Goal.STATUS_NOT_DONE
		)
		self.pending_goal_3 = GoalFactory(
			member=self.member,
			created_by=self.user,
			status=Goal.STATUS_IN_PROGRESS
		)
		self.done_goal = GoalFactory(
			member=self.member,
			created_by=self.user,
			status=Goal.STATUS_DONE
		)

	def test_get_request_succeeds(self):
		response = self.client.get(
			self.url,
			**self.auth_header
		)
		eq_(response.status_code, status.HTTP_200_OK)
		team = Team.objects.get(pk=self.team.pk)
		visible_members = team.members.filter(is_archived=False)
		eq_(len(response.data.get('members')), visible_members.count())
		eq_(
			response.data.get('members')[0].get('id'),
			str(self.member.pk)
		)
		pending_goals = self.member.goals.filter(
			is_archived=False
		)
		eq_(
			len(response.data.get('members')[0].get('goals')),
			pending_goals.count()
		)
		for response_goal in response.data.get('members')[0].get('goals'):
			pending_goal = pending_goals.get(pk=response_goal.get('id'))
			eq_(
				response_goal.get('status'),
				pending_goal.status
			)
			eq_(
				response_goal.get('description'),
				pending_goal.description
			)

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
	Tests /teams/<id>/members/  operations.
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


class TestTeamMemberListTestCase(CustomAPITestCase):
	"""
	Tests /teams/<team_id>/members/<pk>/  operations.
	"""
	def setUp(self):
		super().setUp()

		self.team = TeamFactory(
			name="my team",
			created_by=self.user
		)
		self.member = Member.objects.create(
			name=fake.first_name(),
			email=fake.email(),
			created_by=self.user,
			team=self.team
		)
		self.member_with_user = Member.objects.create(
			name=self.user.first_name,
			email=self.user.email,
			created_by=self.user,
			team=self.team
		)
		self.team_member_url = reverse('team_member-detail', kwargs={
			'team_id': self.team.id,
			'pk': self.member.id,
		})
		self.team_member_with_user_url = reverse('team_member-detail', kwargs={
			'team_id': self.team.id,
			'pk': self.member_with_user.id,
		})

	def test_delete_request_with_valid_data_succeeds(self):
		response = self.client.delete(
			self.team_member_url, **self.auth_header
		)
		eq_(response.status_code, status.HTTP_204_NO_CONTENT)
		member = Member.objects.get(pk=self.member.pk)
		eq_(member.is_archived, True)

	def test_retrieve_request_for_member_without_user_succeeds(self):
		response = self.client.get(
			self.team_member_url, **self.auth_header
		)
		eq_(response.status_code, status.HTTP_200_OK)
		member = Member.objects.get(pk=response.data.get('id'))
		eq_(member.email, response.data.get('email'))
		eq_(str(member.created_by.pk), response.data.get('created_by').get('id'))
		eq_(member.user, response.data.get('user'))

	def test_retrieve_request_for_member_with_user_succeeds(self):
		response = self.client.get(
			self.team_member_with_user_url, **self.auth_header
		)
		eq_(response.status_code, status.HTTP_200_OK)
		member = Member.objects.get(pk=response.data.get('id'))
		eq_(member.email, response.data.get('email'))
		eq_(member.email, response.data.get('email'))
		eq_(str(member.created_by.pk), response.data.get('created_by').get('id'))
		eq_(member.user.pk, response.data.get('user'))


class TestTeamSettingsTestCase(CustomAPITestCase):
	"""
	Tests /teams/<id>/setup/  operations.
	"""
	def setUp(self):
		super().setUp()

		self.team = TeamFactory(
			name="the team",
			created_by=self.user
		)
		self.team.managers.add(self.user)
		self.url = reverse('team-setup', kwargs={'pk': self.team.id})

		self.new_settings_data = {
			'meeting_link': 'https://meet.google.com/xxxxxxxx',
			'slack_webhook': 'https://hooks.slack.com/services/ashsadhdahads',
			'meeting_duration_mins': 20,
			'call_team_method': 'SLACK',
		}

		self.invalid_data = {
			'meeting_link': 'xxxxx',
			'slack_webhook': None,
			'meeting_duration_mins': 'asdasd',
			'call_team_method': 'xxx',
		}

	def test_put_request_with_valid_data_succeeds(self):
		response = self.client.put(
			self.url, self.new_settings_data, **self.auth_header
		)
		eq_(response.status_code, status.HTTP_200_OK)

		team_settings = TeamSettings.objects.get(team=self.team)
		eq_(team_settings.meeting_link, self.new_settings_data.get('meeting_link'))
		eq_(
			team_settings.call_team_method,
			self.new_settings_data.get('call_team_method')
		)
		eq_(
			team_settings.meeting_duration_mins,
			self.new_settings_data.get('meeting_duration_mins')
		)
		eq_(team_settings.slack_webhook, self.new_settings_data.get('slack_webhook'))

	def test_put_request_with_invalid_data_fails(self):
		response = self.client.put(
			self.url, self.invalid_data, **self.auth_header
		)
		eq_(response.status_code, status.HTTP_400_BAD_REQUEST)