from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings


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
    current_version = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.check_data_before_save():
            if self.pk is None:
                super().save(*args, **kwargs)
            else:
                new_version_number = self.current_version + 1
                
                banner_version = BannerVersion.objects.create(
                    banner=self,
                    banner_body=self.get_banner_data(),
                    version_number=new_version_number)

                self.current_version = new_version_number
                super().save(*args, **kwargs)
            # if self.pk is None:
            #     new_version_number = 1
            #     self.current_version = new_version_number
            #     super().save(*args, **kwargs)
            #     BannerVersion.objects.create(
            #         banner=self,
            #         banner_body=self.get_banner_data(),
            #         version_number=new_version_number)
            # else:
            #     current_version_number = self.current_version
            #     new_version_number = current_version_number + 1

            #     BannerVersion.objects.create(
            #         banner=self,
            #         banner_body=self.get_banner_data(),
            #         version_number=new_version_number)
            #     self.current_version = new_version_number
            #     super().save(*args, **kwargs)
        else:
            raise ValueError(
                "Неверные данные. Один баннер может принадлежать одной фиче. \
Не может быть одинаковых тегов у двух баннеров с одинаковыми фичами."
            )

    def check_data_before_save(self):
        features_with_same_id = Banner.objects.exclude(id=self.id).filter(
            feature_id=self.feature_id)
        if features_with_same_id.exists():
            for feature in features_with_same_id:
                if set(self.tag_ids) & set(feature.tag_ids):
                    return False
        return True

    def get_banner_data(self):
        banner_dict = {
                "feature_id": self.feature_id,
                "tag_ids": self.tag_ids,
                "title": self.title,
                "description": self.description,
                "url": self.url,
                "is_active": self.is_active,
                "current_version": self.current_version
            }
        return banner_dict


class BannerVersion(models.Model):
    # banner_id = models.IntegerField(default=0)
    banner = models.ForeignKey(Banner, 
                               on_delete=models.CASCADE, 
                               related_name='versions')
    banner_body = models.JSONField(default=dict)
    version_number = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class AdminToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE, 
                                related_name='admin_token')
    key = models.CharField(max_length=20, unique=True)
    expiration_time = models.DateTimeField(auto_now_add=True)


class UserToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE, 
                                related_name='user_token')
    key = models.CharField(max_length=40, unique=True)
    expiration_time = models.DateTimeField(auto_now_add=True)
