# Generated by Django 5.0.6 on 2024-11-28 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='content',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
