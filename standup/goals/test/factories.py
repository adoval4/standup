import factory


class GoalFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'goals.Goal'
        django_get_or_create = ('description', 'member')

    id = factory.Faker('uuid4')
    description = factory.Sequence(lambda n: f'my goal {n}')
    status = None
    member = None
    set_done_at = None
    set_in_progress_at = None
    set_not_done_at = None
    is_archived = False
    created_by = None