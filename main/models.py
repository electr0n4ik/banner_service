from django.db import models


class Feature(models.Model):
    feature_id = models.IntegerField(unique=True)

class Banner(models.Model):
    feature = models.ForeignKey(
        Feature, 
        on_delete=models.CASCADE)
    
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
    
    is_active = models.BooleanField(
        default=True)

class Tag(models.Model):
    tag_id = models.IntegerField(unique=True)

class BannerTag(models.Model):
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('banner', 'tag')
