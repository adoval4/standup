import factory


class TeamFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'teams.Team'
        django_get_or_create = ('name',)

    id = factory.Faker('uuid4')
    name = factory.Sequence(lambda n: f'test_team{n}')
    is_archived = False
    created_by = None


class MemberFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'teams.Member'
        django_get_or_create = ('name',)

    id = factory.Faker('uuid4')
    email = factory.Faker('email')
    name = factory.Faker('first_name')
    team = None
    is_archived = False
    created_by = None