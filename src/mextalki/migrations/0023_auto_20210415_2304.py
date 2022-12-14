# Generated by Django 3.2 on 2021-04-16 04:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mextalki', '0022_auto_20210409_1004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptiontype',
            name='description',
        ),
        migrations.AddField(
            model_name='subscriptiontype',
            name='include_basic_package',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subscriptiontype',
            name='include_conversation_club',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subscriptiontype',
            name='include_podcast',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subscriptiontype',
            name='include_study_group',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='SubscriptionFeature',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True,
                        primary_key=True, serialize=False, verbose_name='ID',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('feature', models.CharField(max_length=255)),
                (
                    'subscription_type', models.ForeignKey(
                        blank=True, default=None, null=True,
                        on_delete=django.db.models.deletion.PROTECT, related_name='feature', to='mextalki.subscriptiontype',
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
