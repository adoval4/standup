# Utilities
import uuid

# Django
from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

# Models
from standup.utils.models import CustomUserCreatedBaseModel


@python_2_unicode_compatible
class Goal(CustomUserCreatedBaseModel):
	"""Team model.

	Represents a work team.
	"""
	STATUS_DONE = "DONE"
	STATUS_IN_PROGRESS = "IN_PROGRESS"
	STATUS_NOT_DONE = "NOT_DONE"

	STATUSES = (
		(STATUS_DONE, 'Done'),
		(STATUS_IN_PROGRESS, 'In progress'),
		(STATUS_NOT_DONE, 'Not done'),
	)

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	description = models.CharField(max_length=1000)
	member = models.ForeignKey(
		'teams.Member',
		on_delete=models.CASCADE,
		related_name='goals'
	)
	status = models.CharField(
		max_length=12,
		choices=STATUSES,
		null=True,
		default=None
	)
	set_done_at = models.DateTimeField(
		null=True,
		default=None
	)
	set_in_progress_at = models.DateTimeField(
		null=True,
		default=None
	)
	set_not_done_at = models.DateTimeField(
		null=True,
		default=None
	)
	is_archived = models.BooleanField(default=False)

	def __str__(self):
		return u'@{} has goal to {}. (status={})'.format(
			self.member.name,
			self.description,
			self.status
		)
