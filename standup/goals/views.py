# Django rest
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

# Models
from standup.goals.models import Goal

# Permissions
from standup.teams.permissions import IsTeamManager
from standup.goals.permissions import IsTeamManagerOrItsMemberGoal

# Serializers
from standup.goals.serializers import GoalSerializer, CreateGoalSerializer


class GoalViewSet(mixins.UpdateModelMixin,
				  viewsets.GenericViewSet):
	"""
	Creates, updates and archives goals.
	"""

	queryset = Goal.objects.all()

	def get_permissions(self):
		permissions = [ IsTeamManagerOrItsMemberGoal ]
		if self.action in ['create']:
			permissions = [ IsAuthenticated ]
		if self.action in ['destroy']:
			permissions = [ IsAuthenticated, IsTeamManagerOrItsMemberGoal ]
		return [p() for p in permissions]

	def get_serializer_class(self):
		if self.action == 'create':
			return CreateGoalSerializer
		return GoalSerializer

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		goal = serializer.save()
		return Response(
			GoalSerializer(goal).data,
			status=status.HTTP_201_CREATED
		)

	def destroy(self, request, *args, **kwargs):
		"""
		Archives a goals
		"""
		goal = self.get_object()
		goal.is_archived = True
		goal.save()
		return Response(None, status=status.HTTP_204_NO_CONTENT)




