# Generated by Django 5.0.4 on 2024-04-08 10:55

import django.db.models.deletion
import django.utils.timezone
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
            name='content',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='tag_ids',
        ),
        migrations.AddField(
            model_name='banner',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='banner',
            name='description',
            field=models.CharField(blank=True, default='description', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='banner',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='banner',
            name='title',
            field=models.CharField(blank=True, default='title', max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='banner',
            name='url',
            field=models.URLField(blank=True, default='https://www.avito.ru/я-вас-люблю', null=True),
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
        migrations.AlterUniqueTogether(
            name='bannertag',
            unique_together={('banner', 'tag')},
        ),
    ]