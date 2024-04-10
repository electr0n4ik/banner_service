from django.db import models
from django.contrib.postgres.fields import ArrayField


class Banner(models.Model):
    feature_id = models.IntegerField()
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

    def save(self, *args, **kwargs):
        if self.check_data_before_save():
            super().save(*args, **kwargs)
        else:
            raise ValueError(
                "It is impossible to save the banner: \
the uniqueness of tags for feature data is violated."
            )

    def check_data_before_save(self):
        features_with_same_id = Banner.objects.exclude(id=self.id).filter(
            feature_id=self.feature_id)
        if features_with_same_id.exists():

            for feature in features_with_same_id:
                if set(self.tag_ids) & set(feature.tag_ids):
                    return False
        return True
