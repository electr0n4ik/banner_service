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

        if tag_id:
            banner_tags_by_tag = models.BannerTag.objects.filter(
                tag_id=tag_id).select_related("banner")
        else:
            banner_tags_by_tag = models.BannerTag.objects.all()\
                .select_related("banner")
            
        if feature_id:
            filtered_banner_tags = banner_tags_by_tag.filter(
            banner__feature_id=feature_id)
        else:
            filtered_banner_tags = banner_tags_by_tag

        try:
            all_objects = models.Banner.objects.filter(
                bannertag__in=filtered_banner_tags)  # .order_by('id')
        except models.Banner.DoesNotExist:
            all_objects = None

        paginator = Paginator(all_objects, limit)
        current_page = (offset // limit) + 1

        try:
            page = paginator.page(current_page)
        except:
            return JsonResponse([
                "Добавить сюда вывод одного баннера! Или нет баннера"],
                safe=False)

        objects_on_page = page.object_list
        response_data = [{"banner_id": obj.id, 
                          "tag_ids": [obj.tag.id for obj in banner_tags_by_tag\
                                      .filter(banner=obj.id)],
                          "feature_id": obj.title,
                          "content": {
                              "title": obj.title, 
                              "text": obj.description, 
                              "url": obj.url
                          },
                          "is_active": obj.is_active,
                          "created_at": obj.created,
                          "updated_at": obj.modified
                          } for obj in objects_on_page]

        return JsonResponse(
            response_data,
            safe=False,
            status=200)
    
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
    