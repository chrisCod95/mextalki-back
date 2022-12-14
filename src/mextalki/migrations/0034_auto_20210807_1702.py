# Generated by Django 3.2.6 on 2021-08-07 22:02

import sort_order_field.fields
from django.db import migrations, models

import src.mextalki.models.utils


class Migration(migrations.Migration):

    dependencies = [
        ('mextalki', '0033_podcasttest_podcasttestanswer_podcasttestquestion_podcasttestscore'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='podcast',
            options={'ordering': ('sort_order',)},
        ),
        migrations.AddField(
            model_name='podcast',
            name='sort_order',
            field=sort_order_field.fields.SortOrderField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='podcast',
            name='transcript',
            field=models.FileField(
                blank=True, default=None, null=True,
                upload_to=src.mextalki.models.utils.upload_to_v2,
            ),
        ),
    ]
