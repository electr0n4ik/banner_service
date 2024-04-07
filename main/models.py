from django.db import models

class Feature(models.Model):
    feature_id = models.IntegerField(unique=True)

class Banner(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    content = models.JSONField()  # '{"title": "some_title", "text": "some_text", "url": "some_url"}'
    is_active = models.BooleanField(default=True)

class Tag(models.Model):
    tag_id = models.IntegerField(unique=True)

class BannerTag(models.Model):
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
