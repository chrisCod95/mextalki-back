# Generated by Django 3.1.7 on 2021-03-07 01:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mextalki', '0017_auto_20210223_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventtype',
            name='is_conversation_club',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scheduledevent',
            name='location',
            field=models.URLField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='subscriptiontype',
            name='conversation_club_slots',
            field=models.IntegerField(default=0, help_text='set club access slots'),
        ),
        migrations.AddField(
            model_name='useravailablelessontime',
            name='conversation_club_slots',
            field=models.IntegerField(default=0, help_text='set club access slots'),
        ),
        migrations.AlterField(
            model_name='eventtype',
            name='teacher',
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                related_name='event_types', to='mextalki.teacher',
            ),
        ),
        migrations.AlterField(
            model_name='scheduledevent',
            name='teacher',
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                related_name='teacher_scheduled_events', to='mextalki.teacher',
            ),
        ),
    ]
