# Generated by Django 5.1.1 on 2024-10-06 05:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_resident_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='address',
            field=models.TextField(max_length=100, null=True, validators=[django.core.validators.RegexValidator(message='This {field} is required', regex='^(?!\\s*$).+')]),
        ),
        migrations.AlterField(
            model_name='resident',
            name='contact_number',
            field=models.CharField(max_length=100, null=True, validators=[django.core.validators.RegexValidator(message='This {field} is required', regex='^(?!\\s*$).+')]),
        ),
        migrations.AlterField(
            model_name='resident',
            name='full_name',
            field=models.CharField(max_length=100, null=True, validators=[django.core.validators.RegexValidator(message='This {field} is required', regex='^(?!\\s*$).+')]),
        ),
        migrations.AlterField(
            model_name='resident',
            name='landmark',
            field=models.TextField(max_length=100, null=True, validators=[django.core.validators.RegexValidator(message='This {field} is required', regex='^(?!\\s*$).+')]),
        ),
    ]
