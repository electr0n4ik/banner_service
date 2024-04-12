import json

from django.core.cache import cache

from celery import shared_task

@shared_task
def my_periodic_task():
    from . import models
    banners = models.Banner.objects.all()
    banner_data = []

    for banner in banners:
        banner_dict = {
            "feature_id": banner.feature_id,
            "tag_ids": banner.tag_ids,
            "title": banner.title,
            "description": banner.description,
            "url": banner.url,
            "is_active": banner.is_active,
            "created": banner.created.isoformat(),
            "modified": banner.modified.isoformat()
        }
        banner_data.append(banner_dict)
    cache.set("banners", json.dumps(banner_data))
