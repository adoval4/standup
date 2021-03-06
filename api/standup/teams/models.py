# Utilities
import uuid
import jwt

# Django
from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

# Models
from standup.utils.models import CustomUserCreatedBaseModel

# api clients
from standup.utils.apiclients import SlackClient

# email utils
from standup.utils.email import send_mail



@python_2_unicode_compatible
class Team(CustomUserCreatedBaseModel):
	"""Team model.

	Represents a work team.
	"""

	CALL_MESSAGE = 'CALL'
	TO_DO_LIST_MESSAGE = 'TO_DO'

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
		return u'Team "{}" of {} (id={})'.format(
			self.name,
			self.created_by,
			self.id
		)

	@property
	def active_members(self):
		return self.members.filter(is_archived=False).order_by('created')

	@property
	def active_members_emails(self):
		return [ m.email for m in self.active_members.iterator() ]

	def call_team(self):
		self.notify_team(Team.CALL_MESSAGE)

	def send_to_do_list(self):
		self.notify_team(Team.TO_DO_LIST_MESSAGE)

	def notify_team(self, message_type):
		if self.settings.call_team_method == TeamSettings.SLACK:
			if self.settings.slack_webhook is None:
				return None
			self.send_slack_message(message_type)
		elif self.settings.call_team_method == TeamSettings.EMAIL:
			self.send_email(message_type)

	def send_slack_message(self, message_type):
		message = None
		if message_type == Team.CALL_MESSAGE:
			message = render_to_string(
				'team_call_slack.txt',
				{'team': self, 'settings': settings}
			)
		elif message_type == Team.TO_DO_LIST_MESSAGE:
			message = render_to_string(
				'team_to_do_list_slack.txt',
				{'team': self, 'settings': settings}
			)

		if message is not None:
			SlackClient.send_message(self.settings.slack_webhook, message)

	def send_email(self, message_type):
		subject = None
		message = None
		today = timezone.localtime(timezone.now()).date()
		if message_type == Team.CALL_MESSAGE:
			subject = '{} | It\'s time for out standup ({})'.format(self.name, today)
			message = render_to_string(
				'team_call_email.txt',
				{'team': self, 'settings': settings}
			)
		elif message_type == Team.TO_DO_LIST_MESSAGE:
			subject = '{} | Today\'s to do list ({})'.format(self.name, today)
			message = render_to_string(
				'team_to_do_list_email.txt',
				{'team': self, 'settings': settings}
			)

		if None not in [ subject, message ]:
			send_mail(
				subject, message, self.active_members_emails, is_html=True
			)


@python_2_unicode_compatible
class TeamSettings(CustomUserCreatedBaseModel):
	"""Team model.

	Represents a work team.
	"""
	EMAIL = 'EMAIL'
	SLACK = 'SLACK'

	CALL_METHOD = (
		(EMAIL, 'Email'),
		(SLACK, 'Slack')
	)

	team = models.OneToOneField(
		'teams.Team',
		on_delete=models.CASCADE,
		related_name='settings'
	)
	meeting_link = models.URLField(null=True, blank=True, default=None)
	meeting_duration_mins = models.PositiveSmallIntegerField(
		default=10,
		blank=True
	)
	slack_webhook = models.URLField(null=True, blank=True, default=None)
	call_team_method = models.CharField(
		max_length=10,
		choices=CALL_METHOD,
		default=EMAIL
	)

	def __str__(self):
		return u'Team "{}" settings of {} (id={})'.format(
			self.team.name,
			self.team.created_by,
			self.team.id
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

	TOKEN_PAYLOAD_TYPE = 'member_token'

	def __str__(self):
		return u'{} from {} (id={})'.format(
			self.name,
			self.team.name,
			self.id
		)

	@property
	def token(self):
		"""
		Generates member's auth jwt token.
		"""
		return jwt.encode(
			{
				'type': self.TOKEN_PAYLOAD_TYPE,
				'payload':{
					'id': self.pk,
					'email': self.email,
				}
			},
			settings.SECRET_KEY,
			algorithm='HS256'
		).decode('utf-8')

	@property
	def user(self):
		"""
		Return's the associated user (with the same email)
		"""
		from standup.users.models import User
		try:
			return User.objects.get(email=self.email)
		except ObjectDoesNotExist:
			return None

	@staticmethod
	def get_member_from_token(token):
		"""
		Decodes token and retrieves member for it.
		"""
		try:
			data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
		except jwt.exceptions.InvalidTokenError:
			return None
		if data['type'] != Member.TOKEN_PAYLOAD_TYPE:
			return None
		try:
			payload = data.get('payload')
			return Member.objects.get(
				pk=payload.get('id'),
				email=payload.get('email')
			)
		except ObjectDoesNotExist:
			return None
		except KeyError:
			return None

	@property
	def pending_goals(self):
		return self.goals.filter(is_archived=False).order_by('created')

	def send_added_to_team_email(self):
		"""
		Sends an email to member when added to a team. Includes a link for
		the member to create a user if he/she still hasn't.
		"""
		today = timezone.localtime(timezone.now()).date()
		subject = '{} {} just added you to {} ({})'.format(
			self.created_by.first_name,
			self.created_by.last_name,
			self.team.name,
			today
		)
		message = render_to_string(
			'member_added_email.txt',
			{'member': self, 'settings': settings}
		)
		send_mail(
			subject, message, [self.email], is_html=True
		)

@receiver(post_save, sender=Team)
def create_team_settings(sender, instance=None, created=False, **kwargs):
	if created:
		TeamSettings.objects.create(team=instance)
