# Generated by Django 5.1.1 on 2024-10-06 04:44

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_resident_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
