# Utilities
import uuid

# Django
from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

# Models
from standup.utils.models import CustomUserCreatedBaseModel


@python_2_unicode_compatible
class Team(CustomUserCreatedBaseModel):
    """Team model.

    Represents a work team.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=350)
    managers = models.ManyToManyField(
        'users.User',
        related_name="managed_teams",
        help_text=(
            "Managers can add or remove team members and create tasks for them"
        )
    )
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return u'Team {} of {} (id={})'.format(
            self.name,
            self.created_by,
            self.id
        )


@python_2_unicode_compatible
class Member(CustomUserCreatedBaseModel):
    """Member model.

    Represents a team member.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=350)
    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name="members"
    )
    email = models.EmailField()
    is_verified = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return u'{} from {} (id={})'.format(
            self.name,
            self.team.name,
            self.id
        )