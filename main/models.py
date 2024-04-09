from django.db import models
from django.contrib.postgres.fields import ArrayField


class Banner(models.Model):
    feature_id = models.IntegerField(unique=True)
    tag_ids = ArrayField(
        models.IntegerField(unique=True))
    title = models.CharField(
        default="title", 
        max_length=25, 
        blank=True, 
        null=True)
    description = models.CharField(
        default="description", 
        max_length=250, 
        blank=True, 
        null=True)
    url = models.URLField(
        default="https://www.avito.ru/я-вас-люблю", 
        blank=True, 
        null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('feature_id', 'tag_ids')
