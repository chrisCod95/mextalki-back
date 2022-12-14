# Generated by Django 3.1.6 on 2021-02-21 16:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mextalki', '0014_auto_20210213_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptiontype',
            name='has_access_to_courses',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='planpayment',
            name='paypal_payment',
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mextalki.paypalpayment',
            ),
        ),
    ]
