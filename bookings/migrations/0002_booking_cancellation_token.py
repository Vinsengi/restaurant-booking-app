# Generated by Django 5.2.1 on 2025-06-09 10:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='cancellation_token',
            field=models.UUIDField(unique=True, null=True, blank=True),

        ),
    ]
