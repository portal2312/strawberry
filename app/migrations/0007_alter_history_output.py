# Generated by Django 5.0.6 on 2024-05-31 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='output',
            field=models.JSONField(null=True),
        ),
    ]