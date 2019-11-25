# Django rest
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.decorators import action

# Models
from standup.users.models import User

# Permissions
from standup.users.permissions import IsUserOrReadOnly

# Serializers
from standup.users.serializers import CreateUserSerializer, UserSerializer


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
		return Response(UserSerializer(request.user).data)


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


