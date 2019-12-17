# django
from django.urls import reverse

# Utilities
from nose.tools import ok_, eq_
from faker import Faker

# django rest
from rest_framework import status

# models
from standup.goals.models import Goal

# factories
from standup.teams.test.factories import TeamFactory, MemberFactory
from standup.goals.test.factories import GoalFactory

# test utils
from standup.utils.tests import CustomAPITestCase

fake = Faker()


class BaseTestGoalTestCase(CustomAPITestCase):
	"""
	Base setup for both Goal test cases
	"""
	def setUp(self):
		super().setUp()

		self.team = TeamFactory(
			name="my team",
			created_by=self.user
		)
		self.team.managers.add(self.user)

		self.other_team = TeamFactory(
			name="someone else's team",
			created_by=self.user
		)

		self.member = MemberFactory(team=self.team)
		self.not_a_member_of_my_team = MemberFactory(team=self.other_team)



class TestGoalListTestCase(BaseTestGoalTestCase):
	"""
	Tests /goals  operations.
	"""

	def setUp(self):
		super().setUp()

		self.new_goal_data = {
			"member": self.member.pk,
			"description": "Make it work"
		}

		self.url = reverse('goal-list')
		self.url_as_member = '{}?token={}'.format(self.url, self.member.token)

	def test_post_request_with_no_data_fails(self):
		response = self.client.post(self.url, {}, **self.auth_header)
		eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_post_request_without_auth_fails(self):
		response = self.client.post(
			self.url,
			self.new_goal_data
		)
		eq_(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_post_request_as_member_fails(self):
		response = self.client.post(
			self.url_as_member,
			self.new_goal_data
		)
		eq_(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_post_request_for_member_not_from_my_team_fails(self):
		response = self.client.post(
			self.url_as_member,
			{
				"member": self.not_a_member_of_my_team.pk,
				"description": "Make it work"
			},
			**self.auth_header
		)
		eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_post_request_with_valid_data_succeeds(self):
		response = self.client.post(
			self.url,
			self.new_goal_data,
			**self.auth_header
		)
		eq_(response.status_code, status.HTTP_201_CREATED)

		goal = Goal.objects.get(pk=response.data.get('id'))
		eq_(goal.description, self.new_goal_data.get('description'))
		eq_(str(goal.member_id), self.new_goal_data.get('member'))
		eq_(goal.status, None)
		eq_(goal.created_by.email, self.user.email)


class TestGoalDetailTestCase(BaseTestGoalTestCase):
	"""
	Tests /goals/<id>  operations.
	"""

	def setUp(self):
		super().setUp()

		self.goal = GoalFactory(member=self.member, created_by=self.user)

		self.url = reverse('goal-detail', kwargs={'pk': self.goal.pk})
		self.url_as_member = u'{}?token={}'.format(self.url, self.member.token)

	# this is not useful yet, but may in the future
	# def test_destroy_request_with_member_url_succeeds(self):
	# 	response = self.client.delete(
	# 		self.url_as_member
	# 	)
	# 	eq_(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_destroy_request_succeeds(self):
		response = self.client.delete(
			self.url,
			**self.auth_header
		)
		eq_(response.status_code, status.HTTP_204_NO_CONTENT)
		goal = Goal.objects.get(pk=self.goal.pk)
		eq_(goal.is_archived, True)

	# # this is not useful yet, but may in the future
	# def test_partial_update_status_wihtout_auth_succeeds(self):
	# 	response = self.client.patch(
	# 		self.url,
	# 		{
	# 			'status': Goal.STATUS_DONE
	# 		}
	# 	)
	# 	eq_(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_partial_update_name_request_succeeds(self):
		new_goal_description = 'We changed the goal'
		response = self.client.patch(
			self.url,
			{
				'description': new_goal_description
			},
			**self.auth_header
		)
		eq_(response.status_code, status.HTTP_200_OK)
		goal = Goal.objects.get(pk=self.goal.pk)
		eq_(goal.description, new_goal_description)

	def test_partial_update_status_done_request_succeeds(self):
		response = self.client.patch(
			self.url,
			{
				'status': Goal.STATUS_DONE
			},
			**self.auth_header
		)
		eq_(response.status_code, status.HTTP_200_OK)
		goal = Goal.objects.get(pk=self.goal.pk)
		eq_(goal.status, Goal.STATUS_DONE)
		ok_(goal.set_done_at is not None)

	def test_partial_update_status_in_progress_request_succeeds(self):
		response = self.client.patch(
			self.url,
			{
				'status': Goal.STATUS_IN_PROGRESS
			},
			**self.auth_header
		)
		eq_(response.status_code, status.HTTP_200_OK)
		goal = Goal.objects.get(pk=self.goal.pk)
		eq_(goal.status, Goal.STATUS_IN_PROGRESS)
		ok_(goal.set_in_progress_at is not None)

	def test_partial_update_status_not_done_request_succeeds(self):
		response = self.client.patch(
			self.url,
			{
				'status': Goal.STATUS_NOT_DONE
			},
			**self.auth_header
		)
		eq_(response.status_code, status.HTTP_200_OK)
		goal = Goal.objects.get(pk=self.goal.pk)
		eq_(goal.status, Goal.STATUS_NOT_DONE)
		ok_(goal.set_not_done_at is not None)
