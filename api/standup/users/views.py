# Django rest
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

# Models
from standup.users.models import User

# Permissions
from standup.users.permissions import IsUserOrReadOnly

# Serializers
from standup.users.serializers import CreateUserSerializer, UserSerializer
from standup.teams.serializers import TeamSerializer
from standup.goals.serializers import GoalSerializer


class UserViewSet(mixins.RetrieveModelMixin,
				  mixins.UpdateModelMixin,
				  viewsets.GenericViewSet):
	"""
	Updates and retrieves user accounts
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer

	def get_permissions(self):
		permissions = [IsUserOrReadOnly]
		if self.action in ['me']:
			permissions.append(IsAuthenticated)
		return [p() for p in permissions]

	@action(detail=False, methods=["get"])
	def me(self, request, *args, **kwargs):
		user = request.user
		pending_goals = user.pending_goals
		user_data = UserSerializer(user).data
		user_data['teams'] = []
		for team in user.teams.iterator():
			team_data = TeamSerializer(team).data
			team_data['membership'] = team.members.get(
				email=user.email,
				is_archived=False
			).pk
			team_data['im_manager'] = team.managers.filter(pk=user.pk).exists()
			pending_goals_in_team = pending_goals.filter(member__team=team)
			team_data['goals'] = GoalSerializer(
				pending_goals_in_team, many=True
			).data
			user_data['teams'].append(team_data)
		return Response(user_data)


class UserCreateViewSet(mixins.CreateModelMixin,
						viewsets.GenericViewSet):
	"""
	Creates user accounts
	"""
	queryset = User.objects.all()
	serializer_class = CreateUserSerializer
	permission_classes = (AllowAny,)


class CustomAuthToken(ObtainAuthToken):
	"""
	Authenticates user provding it data and token.
	"""
	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(
			data=request.data,
			context={'request': request}
		)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		token = Token.objects.get(user=user)
		user_serializer = UserSerializer(user)
		data = user_serializer.data
		data['token'] = token.key
		return Response(data)


