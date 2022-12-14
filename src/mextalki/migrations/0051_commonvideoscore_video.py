# Generated by Django 3.2.9 on 2022-01-19 22:08

import django.db.models.deletion
import sort_order_field.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mextalki', '0050_videoscore'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True,
                        primary_key=True, serialize=False, verbose_name='ID',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sort_order', sort_order_field.fields.SortOrderField(db_index=True, default=0)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('thumbnail_url', models.CharField(max_length=255)),
                ('youtube_video_id', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('slug', models.SlugField(default='')),
            ],
            options={
                'ordering': ('sort_order',),
            },
        ),
        migrations.CreateModel(
            name='CommonVideoScore',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True,
                        primary_key=True, serialize=False, verbose_name='ID',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exp_points', models.IntegerField(default=0)),
                ('user_already_get_points', models.BooleanField(default=False)),
                (
                    'user', models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='common_video_scores', to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'video', models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='common_video_scores', to='mextalki.video',
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
