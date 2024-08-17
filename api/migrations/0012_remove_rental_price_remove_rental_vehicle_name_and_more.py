# Generated by Django 5.0.6 on 2024-08-17 04:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_profile_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rental',
            name='price',
        ),
        migrations.RemoveField(
            model_name='rental',
            name='vehicle_name',
        ),
        migrations.RemoveField(
            model_name='rental',
            name='vehicle_type',
        ),
        migrations.AlterField(
            model_name='rental',
            name='images',
            field=models.FileField(upload_to='rentals/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])]),
        ),
    ]
