# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from standup.users.models import User, Profile


@admin.register(User)
class UserAdmin(UserAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
