# Generated by Django 5.0.6 on 2024-11-19 06:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_remove_message_room_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RateOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates_received', to=settings.AUTH_USER_MODEL)),
                ('rate_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates_given', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]