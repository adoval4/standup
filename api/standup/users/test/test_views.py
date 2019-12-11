# django
from django.urls import reverse
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import check_password

# django rest
from rest_framework.test import APITestCase
from rest_framework import status

# utilities
from nose.tools import ok_, eq_
from faker import Faker

# models
from standup.users.models import User

# factories
from standup.users.test.factories import UserFactory
from standup.teams.test.factories import TeamFactory, MemberFactory
from standup.goals.test.factories import GoalFactory

fake = Faker()


class TestUserListTestCase(APITestCase):
    """
    Tests /users list operations.
    """

    def setUp(self):
        self.url = reverse('user-list')
        self.user_data = model_to_dict(UserFactory.build())

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_request_with_valid_data_succeeds(self):
        response = self.client.post(self.url, self.user_data)
        eq_(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(pk=response.data.get('id'))
        eq_(user.email, self.user_data.get('email'))
        ok_(check_password(self.user_data.get('password'), user.password))


class TestUserDetailTestCase(APITestCase):
    """
    Tests /users/<id> operations.
    """

    def setUp(self):
        self.user = UserFactory()
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')

    def test_get_request_returns_a_given_user(self):
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_200_OK)

    def test_put_request_updates_a_user(self):
        new_first_name = fake.first_name()
        payload = {'first_name': new_first_name}
        response = self.client.put(self.url, payload)
        eq_(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(pk=self.user.id)
        eq_(user.first_name, new_first_name)


class TestUserDetailTestCase(APITestCase):
    """
    Tests /users/me operations.
    """

    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.url = reverse('user-me')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')

        self.team_1 = TeamFactory(
			name="my team 1, where im a manager",
			created_by=self.user
		)
        self.team_1.managers.add(self.user)
        self.team_1_membership = MemberFactory(
            team=self.team_1, email=self.user.email
        )
        self.goal_1 = GoalFactory(member=self.team_1_membership)

        self.team_2 = TeamFactory(
			name="my team 2, where im not a manager",
			created_by=self.other_user
		)
        self.team_2.managers.add(self.other_user)
        self.team_2_membership = MemberFactory(
            team=self.team_2, email=self.user.email
        )
        self.goal_2 = GoalFactory(member=self.team_2_membership)
        self.archived_goal = GoalFactory(member=self.team_2_membership, is_archived=True)


    def test_get_request_returns_a_given_user(self):
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        eq_(response_data.get('id'), self.user.pk)
        eq_(len(response_data.get('teams')), self.user.memberships.count())

        team_1_data = response_data.get('teams')[0]
        eq_(team_1_data.get('id'), self.team_1.pk)
        eq_(team_1_data.get('name'), self.team_1.name)
        eq_(team_1_data.get('im_manager'), True)

        team_1_pending_goals_data = team_1_data.get('goals')
        eq_(len(team_1_pending_goals_data), 1)
        eq_(team_1_pending_goals_data[0].get('id'), self.goal_1.pk)

        team_2_data = response_data.get('teams')[1]
        eq_(team_2_data.get('id'), self.team_2.pk)
        eq_(team_2_data.get('name'), self.team_2.name)
        eq_(team_2_data.get('im_manager'), False)

        team_2_pending_goals_data = team_2_data.get('goals')
        eq_(len(team_2_pending_goals_data), 1)
        eq_(team_2_pending_goals_data[0].get('id'), self.goal_2.pk)
