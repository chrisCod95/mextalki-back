# Generated by Django 3.2.14 on 2022-08-12 03:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mextalki', '0066_alter_comment_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event_status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('CANCELLED', 'CANCELLED'), ('RESCHEDULED', 'RESCHEDULED')], default='ACTIVE', max_length=24)),
                ('reminder_schedule', models.DateTimeField()),
                ('reminder_was_sent', models.BooleanField(default=False)),
                ('scheduled_event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reminders', to='mextalki.scheduledevent')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='event_reminders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Scheduled Events - Reminders',
            },
        ),
    ]
