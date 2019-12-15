# django
from django.core.management.base import BaseCommand, CommandError

# models
from standup.users.models import User
from standup.teams.models import Team


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        # create super user
        email = input('Email: ')
        first_name = input('First name: ')
        last_name = input('Last name: ')
        password = input('Password: ')
        user = User.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        team_name = input('Team\'s name: ')
        team = Team.objects.create(name=team_name)
        team.managers.add(user)