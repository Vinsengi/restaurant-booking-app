# Generated by Django 5.2.1 on 2025-06-11 13:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_auto_20250609_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='cancellation_token',
            field=models.UUIDField(blank=True, default=uuid.uuid4, null=True, unique=True),
        ),
    ]
