# Generated by Django 5.0.4 on 2024-04-07 07:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='banner',
            name='unique_banner_tag',
        ),
        migrations.RenameField(
            model_name='banner',
            old_name='feature_id',
            new_name='feature',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='tag_ids',
        ),
        migrations.AddField(
            model_name='bannertag',
            name='banner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.banner'),
        ),
        migrations.AddField(
            model_name='bannertag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tag'),
        ),
    ]
