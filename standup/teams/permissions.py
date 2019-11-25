from rest_framework import permissions


class IsTeamManager(permissions.BasePermission):
    """
    Validates that the user is a member of the view team.
    """

    def has_permission(self, request, view):
        q = request.user.managed_teams.filter(pk=view.team.pk)
        return q.count() > 0


class IsTeamCreator(permissions.BasePermission):
    """
    Validates user created the team.
    """

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user
