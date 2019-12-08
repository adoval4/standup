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
