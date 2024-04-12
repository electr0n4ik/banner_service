import json

from django.core.cache import cache

from celery import shared_task

from . import models

@shared_task
def my_periodic_task():
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
            "modified": banner.modified.isoformat(),
            "current_version": banner.current_version
        }
        banner_data.append(banner_dict)
    cache.set("banners", json.dumps(banner_data))

@shared_task
def my_task_to_del_banners(feature_id=None, tag_id=None):
    if not tag_id and not feature_id:
        return False

    banners_to_delete = models.Banner.objects.all()

    if tag_id:
        banners_to_delete = banners_to_delete.filter(tag_ids__contains=[tag_id])

    elif feature_id:
        banners_to_delete = banners_to_delete.filter(feature_id=feature_id)

    deleted_count, _ = banners_to_delete.delete()
    