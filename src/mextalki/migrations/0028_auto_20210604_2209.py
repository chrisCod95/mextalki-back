# Generated by Django 3.2 on 2021-06-05 03:09

from django.db import migrations, models

import src.mextalki.models.utils


class Migration(migrations.Migration):

    dependencies = [
        ('mextalki', '0027_auto_20210511_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptiontype',
            name='include_podcast',
        ),
        migrations.RemoveField(
            model_name='subscriptiontype',
            name='include_study_group',
        ),
        migrations.AlterField(
            model_name='conversationclubtestimonial',
            name='flag_thumbnail',
            field=models.ImageField(upload_to=src.mextalki.models.utils.upload_to_v2),
        ),
        migrations.AlterField(
            model_name='conversationclubtestimonial',
            name='thumbnail',
            field=models.ImageField(upload_to=src.mextalki.models.utils.upload_to_v2),
        ),
    ]