# django rest
from rest_framework import permissions

# Models
from standup.teams.models import Member


def get_member_from_request(request):
	"""
	Returns a member according to the provided token in request. Returns None
	in case token was not provided, is invalid or there is no member for it.
	"""
	try:
		member_token = request.query_params['token']
	except KeyError:
		return None
	return Member.get_member_from_token(member_token)


class IsTeamManagerOrItsMemberGoal(permissions.BasePermission):
    """
    Validates that the user is a manager of the team or own the goal.
    """

    def is_team_manager(self, request, goal):
        """
        Check if its a team manager
        """
        if request.user.is_anonymous:
            return False
        q = request.user.managed_teams.filter(pk=goal.member.team_id)
        return q.count() > 0

    def has_object_permission(self, request, view, obj):
        if self.is_team_manager(request, obj):
            return True
		# if goal's member user is the same as the one making the request 
        return obj.member.user == request.user


