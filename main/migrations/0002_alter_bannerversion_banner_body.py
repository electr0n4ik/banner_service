# Generated by Django 5.0.4 on 2024-04-12 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerversion',
            name='banner_body',
            field=models.JSONField(default=dict),
        ),
    ]
