# Generated by Django 2.1.11 on 2019-11-25 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created.', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the object was last modified.', verbose_name='modified at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=1000)),
                ('status', models.CharField(choices=[('DONE', 'Done'), ('IN_PROGRESS', 'In progress'), ('IN_PROGRESS', 'Not done')], default=None, max_length=12, null=True)),
                ('set_done_at', models.DateTimeField(default=None, null=True)),
                ('set_in_progress_at', models.DateTimeField(default=None, null=True)),
                ('set_not_done_at', models.DateTimeField(default=None, null=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goals', to='teams.Member')),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]