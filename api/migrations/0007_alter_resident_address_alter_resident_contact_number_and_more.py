# Generated by Django 5.1.1 on 2024-10-06 05:04

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_resident_address_alter_resident_contact_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='address',
            field=models.TextField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='resident',
            name='contact_number',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='resident',
            name='full_name',
            field=models.TextField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='resident',
            name='id',
            field=models.UUIDField(default=uuid.uuid5, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='resident',
            name='landmark',
            field=models.TextField(max_length=100, null=True),
        ),
    ]
