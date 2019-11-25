# django
from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView

# django rest
from rest_framework.routers import DefaultRouter

# views
from standup.users.views import UserViewSet, UserCreateViewSet, CustomAuthToken
from standup.teams.views import TeamViewSet, TeamMemberViewSet
from standup.goals.views import GoalViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, base_name="user")
router.register(r'users', UserCreateViewSet, base_name="user")
router.register(r'teams', TeamViewSet, base_name="team")
router.register(
    r'teams/(?P<team_id>[0-9a-f-]+)/members',
    TeamMemberViewSet,
    base_name="team_member"
)
router.register(r'goals', GoalViewSet, base_name="goal")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', CustomAuthToken),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
