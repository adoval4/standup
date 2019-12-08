# django
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

# Django rest
from rest_framework import serializers

# Models
from standup.goals.models import Goal
from standup.teams.models import Member



class GoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = (
            'id',
            'description',
            'created',
            'status'
        )

    def update(self, instance, validated_data):
        """
        Check if status was updated to updated related DateTimeFields
        """
        instance = super().update(instance, validated_data)

        if 'status' not in validated_data:
            return instance

        new_status = validated_data.get('status')
        now = timezone.now()
        if new_status == Goal.STATUS_DONE:
            instance.set_done_at = now
        if new_status == Goal.STATUS_IN_PROGRESS:
            instance.set_in_progress_at = now
        if new_status == Goal.STATUS_NOT_DONE:
            instance.set_not_done_at = now

        instance.save()
        return instance

class CreateGoalSerializer(serializers.Serializer):

    member = serializers.CharField(min_length=1, max_length=100)
    description = serializers.CharField(min_length=1, max_length=1000)
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate_member(self, member):
        """
        - Validates that member exists.
        - Valdidates that user is his manager
        """
        try:
            member = Member.objects.get(pk=member)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Member does not exist.'
            )

        user = self.context['request'].user
        user_managed_teams = user.managed_teams.filter(is_archived=False)
        q = user_managed_teams.filter(pk=member.team_id)
        if q.exists() is False:
            raise serializers.ValidationError(
                'User is not manager of member.'
            )
        return member

    def create(self, validated_data):
        """
        Creates team and as user as manager
        """
        return Goal.objects.create(**validated_data)
