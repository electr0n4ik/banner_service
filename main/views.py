from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from . import models


@csrf_exempt
def user_banner_view(request):
    if request.method == 'GET':
        tag_id = request.GET.get("tag_id", None)
        feature_id = request.GET.get("feature_id", None)

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
        return JsonResponse({
            "content":"Получение всех баннеров c фильтрацией по фиче и/или тегу"
            }, status=200)
    elif request.method == 'POST':
        return JsonResponse({
            "content":"Создание нового баннера"
            }, status=201)
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
    