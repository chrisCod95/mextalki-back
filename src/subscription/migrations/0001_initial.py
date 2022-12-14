# Generated by Django 3.2.13 on 2022-04-27 03:11

import uuid

import colorfield.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionType',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True,
                        primary_key=True, serialize=False, verbose_name='ID',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                (
                    'currency', models.CharField(
                        choices=[
                            ('USD', 'USD'), ('MXN', 'MXN'),
                        ], default='USD', max_length=3,
                    ),
                ),
                ('active', models.BooleanField(default=True)),
                (
                    'color', colorfield.fields.ColorField(
                        default='#FFFFFF',
                        image_field=None, max_length=18, samples=None,
                    ),
                ),
                (
                    'billing_cycle', models.CharField(
                        choices=[
                            ('WEEK', 'WEEKLY'), ('MONTH', 'MONTHLY'), ('YEAR', 'YEARLY'),
                        ], default='MONTH', max_length=10,
                    ),
                ),
                ('paypal_plan_id', models.CharField(blank=True, max_length=50, null=True)),
                ('stripe_price_id', models.CharField(blank=True, max_length=50, null=True)),
                ('lesson_time', models.IntegerField(default=0, help_text='Set in hours')),
                ('practice_time', models.IntegerField(default=0, help_text='Set in hours')),
                (
                    'extra_hour_lesson_price', models.FloatField(
                        default=0, help_text='Lesson extra Hour price',
                    ),
                ),
                (
                    'extra_hour_practice_price', models.FloatField(
                        default=0, help_text='Practice extra Hour price',
                    ),
                ),
                (
                    'extra_hour_currency', models.CharField(
                        choices=[
                            ('USD', 'USD'), ('MXN', 'MXN'),
                        ], default='USD', max_length=3,
                    ),
                ),
                (
                    'conversation_club_slots', models.IntegerField(
                        default=0, help_text='set club access slots',
                    ),
                ),
                ('has_access_to_courses', models.BooleanField(default=True)),
                ('include_basic_package', models.BooleanField(default=False)),
                ('include_conversation_club', models.BooleanField(default=False)),
                ('include_podcast_features', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('price',),
            },
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
                        on_delete=django.db.models.deletion.PROTECT, related_name='feature', to='subscription.subscriptiontype',
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                (
                    'id', models.UUIDField(
                        default=uuid.uuid4,
                        editable=False, primary_key=True, serialize=False,
                    ),
                ),
                ('active', models.BooleanField(default=False)),
                (
                    'status', models.CharField(
                        choices=[
                            ('CREATED', 'CREATED'), ('ACTIVE', 'ACTIVE'), (
                                'CANCELLED', 'CANCELLED',
                            ), ('EXPIRED', 'EXPIRED'),
                        ], default='CREATED', max_length=24,
                    ),
                ),
                ('next_billing_time', models.DateTimeField(blank=True, null=True)),
                (
                    'provider', models.CharField(
                        choices=[
                            ('PAYPAL', 'PAYPAL'), ('STRIPE', 'STRIPE'),
                        ], max_length=10,
                    ),
                ),
                ('provider_id', models.CharField(blank=True, max_length=50, null=True)),
                (
                    'subscription_type', models.ForeignKey(
                        blank=True, null=True,
                        on_delete=django.db.models.deletion.PROTECT, to='subscription.subscriptiontype',
                    ),
                ),
                (
                    'user', models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                        related_name='subscriptions', to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
