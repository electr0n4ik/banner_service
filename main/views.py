import json

from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from . import models


@csrf_exempt
def user_banner_view(request):
    if request.method == 'GET':
        tag_id = request.GET.get("tag_id", None)  #TODO: required: true  -> 400
        feature_id = request.GET.get("feature_id", None)  #TODO: required: true -> 400

        banner_tags_by_tag = models.BannerTag.objects.filter(tag_id=tag_id)
        filtered_banner_tags = banner_tags_by_tag.filter(
            banner__feature_id=feature_id)
        try:
            banner = models.Banner.objects.get(
                bannertag__in=filtered_banner_tags)
        except models.Banner.DoesNotExist:
            banner = None
        if banner:
            return JsonResponse({
                "title": banner.title, 
                "text": banner.description, 
                "url": banner.url
                }, status=200)
        else:
            return JsonResponse({
                "error": "Баннер для данной фичи и тега не найден"
            }, status=404)
    else:
        return JsonResponse({
            'error': 'Method not allowed'
            }, status=405)


@csrf_exempt
def banners_view(request):
    if request.method == 'GET':
        tag_id = request.GET.get("tag_id", None)
        feature_id = request.GET.get("feature_id", None)
        limit = int(request.GET.get('limit', 100))
        offset = int(request.GET.get('offset', 0))

        banners = models.Banner.objects.all()

        if tag_id:
            banners = banners.filter(tag_ids__contains=[int(tag_id)])

        if feature_id:
            banners = banners.filter(feature_id=int(feature_id))

        paginator = Paginator(banners, limit)
        current_page = (offset // limit) + 1

        try:
            page = paginator.page(current_page)
        except:
            return JsonResponse([
                "Добавить сюда вывод одного баннера! Или нет баннера"],
                safe=False)

        objects_on_page = page.object_list
        response_data = [f"count: {len(objects_on_page)}"]
        
        for obj in objects_on_page:

            response_data.append({
                "banner_id": obj.id,
                "tag_ids": obj.tag_ids,
                "feature_id": obj.feature_id,
                "content": {
                    "title": obj.title,
                    "text": obj.description,
                    "url": obj.url
                },
                "is_active": obj.is_active,
                "created_at": obj.created,
                "updated_at": obj.modified
            })

        return JsonResponse(
            response_data,
            safe=False,
            status=200)
    
    elif request.method == 'POST':
        # {
        #     "tag_ids": [1, 2],

        #     "feature_id": 1,

        #     "content": {
        #         "title": "new_title", 
        #         "text": "new_text", 
        #         "url": "new_url"
        #     },

        #     "is_active": true
        # }
        data = json.loads(request.body.decode('utf-8'))
        tag_ids = data.get("tag_ids")
        feature_id = data.get("feature_id")
        content = data.get("content")
        is_active = data.get("is_active")

        feature, _ = models.Feature.objects.get_or_create(
            feature_id=feature_id)

        banner = models.Banner.objects.create(
            feature=feature,
            title=content.get("title"),
            description=content.get("text"),
            url=content.get("url"),
            is_active=is_active
        )

        for tag_id in tag_ids:
            tag, _ = models.Tag.objects.get_or_create(tag_id=tag_id)
            models.BannerTag.objects.create(banner=banner, tag=tag)

        return JsonResponse({
            "banner_id": banner.id
            },
            status=201)
    
        #IntegrityError если нарушена уникальность
    
    else:
        return JsonResponse({
            'error': 'Method not allowed'
            }, status=405)


@csrf_exempt
def banner_view(request, id):
    if request.method == 'PATCH':
        return JsonResponse({
            "content":f"Обновление содержимого баннера {id}"
            }, status=200)
    elif request.method == 'DELETE':
        return JsonResponse({
            "content": f"Удаление баннера по идентификатору {id}"
            }, status=204)
    else:
        return JsonResponse({
            'error': 'Method not allowed'
            }, status=405)
    