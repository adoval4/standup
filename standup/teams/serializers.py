# Django rest
from rest_framework import serializers

# Models
from standup.teams.models import Team, Member


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('id', 'name')


class CreateTeamSerializer(serializers.Serializer):

    name = serializers.CharField(min_length=2)
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate_name(self, name):
        """
        Validates that user has no team with same name
        """
        # make name lowercase
        name = name.lower()
        # check if user has a team with same name
        user = self.context['request'].user
        q = Team.objects.filter(
            name=name,
            is_archived=False,
            created_by=user
        )
        if q.exists():
            raise serializers.ValidationError(
                'Already have a team with same name.'
            )
        return name

    def create(self, validated_data):
        """
        Creates team and as user as manager
        """
        user = self.context['request'].user
        team = Team.objects.create(**validated_data)
        team.managers.add(user)
        return team


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ('id', 'name', 'email')
        read_only_fields = ('email', )


class CreateTeamMemberSerializer(serializers.Serializer):

    name = serializers.CharField(min_length=2)
    email = serializers.EmailField()
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate_name(self, name):
        """
        Validates that there is no other memeber with same name in team.
        """
        team = self.context['team']
        q = team.members.filter(name=name, is_archived=False)
        if q.exists():
            raise serializers.ValidationError(
                'Already exists a member with this name.'
            )
        return name

    def validate_email(self, email):
        """
        Validates that there is no other member with same email in team.
        """
        team = self.context['team']
        q = team.members.filter(email=email, is_archived=False)
        if q.exists():
            raise serializers.ValidationError(
                'Already exists a member with this email.'
            )
        return email

    def create(self, validated_data):
        """
        Creates member for team
        """
        team = self.context['team']
        member = Member.objects.create(team=team, **validated_data)
        return member