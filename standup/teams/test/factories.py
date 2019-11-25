import factory


class TeamFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'teams.Team'
        django_get_or_create = ('name',)

    id = factory.Faker('uuid4')
    name = factory.Sequence(lambda n: f'test_team{n}')
    is_archived = False
    created_by = None