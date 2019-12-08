# Generated by Django 2.1.11 on 2019-12-04 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='status',
            field=models.CharField(choices=[('DONE', 'Done'), ('IN_PROGRESS', 'In progress'), ('NOT_DONE', 'Not done')], default=None, max_length=12, null=True),
        ),
    ]