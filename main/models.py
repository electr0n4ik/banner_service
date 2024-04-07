from django.db import models


class Feature(models.Model):
    feature_id =  models.IntegerField(unique=True)

class Banner(models.Model):
    tag_ids = models.ManyToManyField('Tag', related_name='tags')
    feature_id = models.ForeignKey(Feature, on_delete=models.CASCADE)
    content = models.JSONField()  # '{"title": "some_title", "text": "some_text", "url": "some_url"}'
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['feature_id'], name='unique_banner_tag')
        ]


class Tag(models.Model):
    tag_id = models.IntegerField(unique=True)
