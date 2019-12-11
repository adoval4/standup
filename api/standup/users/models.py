# Utilities
import uuid

# Django
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save

# Rest framework
from rest_framework.authtoken.models import Token

# Models
from standup.utils.models import CustomBaseModel
from standup.teams.models import Team, Member
from standup.goals.models import Goal


@python_2_unicode_compatible
class User(AbstractUser):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	email = models.EmailField(
		'email address',
		unique=True,
		error_messages={
			'unique': 'A user with that email already exists.'
		}
	)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']

	def __str__(self):
		return self.email

	@property
	def memberships(self):
		return Member.objects.filter(email=self.email)

	@property
	def teams(self):
		team_ids = self.memberships.values_list(
			'team', flat=True
		)
		return Team.objects.filter(pk__in=team_ids).order_by('created')

	@property
	def pending_goals(self):
		return Goal.objects.filter(
			member__email=self.email,
			is_archived=False
		).order_by('created')


@python_2_unicode_compatible
class Profile(CustomBaseModel):
	"""Profile model.

	A profile holds a user's public data like picture and more.
	"""

	user = models.OneToOneField('users.User', on_delete=models.CASCADE)

	picture = models.ImageField(
		'profile picture',
		upload_to='users/pictures/',
		blank=True,
		null=True
	)

	def __str__(self):
		return str(self.user)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)
		Profile.objects.create(user=instance)
