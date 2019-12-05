# Django
from django.contrib import admin

# Models
from standup.teams.models import Team, Member, TeamSettings


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass


@admin.register(TeamSettings)
class TeamSettingsAdmin(admin.ModelAdmin):
    pass

