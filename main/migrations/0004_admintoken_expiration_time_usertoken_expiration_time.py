# Generated by Django 5.0.4 on 2024-04-11 13:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_admintoken_usertoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='admintoken',
            name='expiration_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usertoken',
            name='expiration_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
