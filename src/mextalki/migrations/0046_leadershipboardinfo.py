# Generated by Django 3.2.7 on 2021-11-05 02:11

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mextalki', '0045_alter_leadershipscore_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeadershipBoardInfo',
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
                ('active', models.BooleanField(default=True)),
                ('how_get_points', tinymce.models.HTMLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
