# Generated by Django 5.0.6 on 2024-05-30 06:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_fruit_wiki_urls'),
    ]

    operations = [
        migrations.AddField(
            model_name='fruit',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
