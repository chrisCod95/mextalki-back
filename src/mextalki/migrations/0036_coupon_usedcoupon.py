# Generated by Django 3.2.4 on 2021-09-18 03:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mextalki', '0035_maskcopy_maskinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True,
                        primary_key=True, serialize=False, verbose_name='ID',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('discount', models.FloatField(default=0)),
                ('times_used', models.IntegerField(default=0)),
                ('times_used_limit', models.IntegerField(default=0)),
                (
                    'owner', models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                        related_name='owners', to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UsedCoupon',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True,
                        primary_key=True, serialize=False, verbose_name='ID',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                (
                    'coupon', models.ForeignKey(
                        blank=True, null=True,
                        on_delete=django.db.models.deletion.PROTECT, related_name='coupons', to='mextalki.coupon',
                    ),
                ),
                (
                    'user', models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                        related_name='users', to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
    ]