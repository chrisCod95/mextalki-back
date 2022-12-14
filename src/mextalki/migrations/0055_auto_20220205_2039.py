# Generated by Django 3.2.11 on 2022-02-05 20:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20211109_1822'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mextalki', '0054_referral'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserReferralCredits',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                (
                    'user', models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True, related_name='user_credits', serialize=False, to='users.user',
                    ),
                ),
                ('credits', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='referral',
            name='user',
            field=models.OneToOneField(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                related_name='referral', to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
