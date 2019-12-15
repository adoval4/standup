# django
from django.db import transaction

# Django rest
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

# Models
from standup.teams.models import Team, Member
from standup.goals.models import Goal

# Permissions
from standup.teams.permissions import (
	IsTeamManager,
	IsTeamCreator,
	IsTeamManagerOfObject
)

# Serializers
from standup.teams.serializers import (
	TeamSerializer,
	CreateTeamSerializer,
	MemberSerializer,
	CreateTeamMemberSerializer,
	TeamSettingsSerializer,
	TeamManagerSerializer
)
from standup.users.serializers import UserSerializer
from standup.goals.serializers import GoalSerializer


class TeamViewSet(mixins.RetrieveModelMixin,
				  mixins.UpdateModelMixin,
				  viewsets.GenericViewSet):
	"""
	Creates, lists, updates and archives teams.
	"""

	queryset = Team.objects.all()

	def get_permissions(self):
		permissions = []
		if self.action in ['create', 'list']:
			permissions.append(IsAuthenticated)
		if self.action in ['update', 'partial_update']:
			permissions.append(IsTeamCreator)
		if self.action in ['archive_done', 'call']:
			permissions.append(IsTeamManagerOfObject)
		return [p() for p in permissions]

	def get_serializer_class(self):
		if self.action == 'create':
			return CreateTeamSerializer
		return TeamSerializer

	def list(self, request, *args, **kwargs):
		user = self.request.user
		queryset = user.managed_teams.filter(
			is_archived=False
		).order_by('created')
		queryset = self.filter_queryset(queryset)

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		team = serializer.save()
		return Response(
			TeamSerializer(team).data,
			status=status.HTTP_201_CREATED
		)

	def destroy(self, request, *args, **kwargs):
		"""
		Archives a team
		"""
		team = self.get_object()
		team.is_archived = True
		team.save()
		return Response(None, status=status.HTTP_204_NO_CONTENT)

	def retrieve(self, request, *args, **kwargs):
		"""
		Returns team, members and goals.
		"""
		team = self.get_object()
		data = self.get_serializer(team).data
		data['settings'] = TeamSettingsSerializer(team.settings).data
		data['managers'] = TeamManagerSerializer(team.managers, many=True).data
		data['members'] = []
		members_q = team.active_members
		for member in team.active_members.iterator():
			member_data = MemberSerializer(member).data
			# get member's pending goals
			member_data['goals'] = GoalSerializer(
				member.pending_goals,
				many=True
			).data
			data['members'].append(member_data)
		return Response(data)

	@action(detail=True, methods=['put'])
	def setup(self, request, *args, **kwargs):
		"""
		Updates team settings
		"""
		team = self.get_object()
		serializer = TeamSettingsSerializer(team.settings, data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)

	@action(detail=True, methods=['get'])
	def call(self, request, *args, **kwargs):
		team = self.get_object()
		team.call_team()
		return Response(None, status=status.HTTP_200_OK)

	@action(detail=True, methods=['delete'])
	def archive_done(self, request, *args, **kwargs):
		team = self.get_object()
		done_unarchived_goals = Goal.objects.filter(
			is_archived=False,
			status=Goal.STATUS_DONE,
			member__team=team
		)
		with transaction.atomic():
			for goal in done_unarchived_goals.iterator():
				goal.is_archived = True
				goal.save()

		team.send_to_do_list()

		return Response(None, status=status.HTTP_204_NO_CONTENT)


class TeamMemberViewSet(
	mixins.RetrieveModelMixin,
	viewsets.GenericViewSet):
	"""
	Creates and archives team members of a team
	"""

	def dispatch(self, request, *args, **kwargs):
		"""
		Verify that team exists.
		"""
		team_id = kwargs['team_id']
		self.team = get_object_or_404(Team, pk=team_id)
		return super(TeamMemberViewSet, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		return self.team.members.filter(is_archived=False)

	def get_permissions(self):
		permissions = [ AllowAny ]
		if self.action in ['update', 'partial_update', 'create']:
			permissions += [IsAuthenticated, IsTeamManager]
		return [p() for p in permissions]

	def get_serializer_class(self):
		if self.action in ['create', 'destroy']:
			return CreateTeamMemberSerializer
		return MemberSerializer

	def get_serializer_context(self):
		"""Add team to serializer context."""
		context = super(TeamMemberViewSet, self).get_serializer_context()
		context['team'] = self.team
		return context

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		member = serializer.save()
		return Response(
			MemberSerializer(member).data,
			status=status.HTTP_201_CREATED
		)

	def retrieve(self, request, *args, **kwargs):
		"""
		Retrieves member info but appends extra info such as if the member's
		email already has a user.
		"""
		response = super(TeamMemberViewSet, self).retrieve(
			request, *args, **kwargs
		)
		member = self.get_object()
		member_user = member.user
		data = response.data
		data['team'] = TeamSerializer(member.team).data
		data['created_by'] = UserSerializer(member.created_by).data
		data['user'] = None
		if member_user:
			data['user'] = member_user.pk
		return Response(data)

	def destroy(self, request, *args, **kwargs):
		"""
		Archives a team member
		"""
		member = self.get_object()
		member.is_archived = True
		member.save()
		return Response(None, status=status.HTTP_204_NO_CONTENT)




