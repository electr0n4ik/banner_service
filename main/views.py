from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from . import models


@csrf_exempt
def user_banner_view(request):
    if request.method == 'GET':
        tag_id = request.GET.get("tag_id", None)
        feature_id = request.GET.get("feature_id", None)

        # banners = models.Banner.objects.filter(feature=feature_id)
        # banner_tag = models.BannerTag.objects.filter(
        #     tag_id=tag_id,
        #     banner__feature_id=feature_id
        # ).select_related("banner", "tag").all()
        # Получение всех баннеров, связанных с конкретным тегом и функцией через модель BannerTag
        # banners = models.Banner.objects.filter(
        #     bannertag__tag_id=tag_id,
        #     feature_id=feature_id,
        #     bannertag__isnull=False  # Условие для проверки наличия связанных объектов BannerTag
        # )
        # Получение всех баннеров, связанных с конкретной функцией (feature)
        banners_by_feature = models.Banner.objects.filter(feature_id=feature_id)
        print("Banners by feature IDs:", list(banners_by_feature.values_list('id', flat=True)))

        # Получение всех объектов BannerTag, связанных с указанным тегом
        banner_tags_by_tag = models.BannerTag.objects.filter(tag_id=tag_id)
        print("Banner tags by tag IDs:", list(banner_tags_by_tag.values_list('id', flat=True)))

        # Находим общие баннеры между двумя наборами
        # banners = banner_tags_by_tag.filter(banner__in=banners_by_feature)
        # print("Common banner tags IDs:", list(banners.values_list('id', flat=True)))
        banners = models.Banner.objects.filter(bannertag__in=banner_tags_by_tag)
        print("Common banners IDs:", list(banners.values_list('id', flat=True)))

        for i in banners:
            print(i)
            banner = i
        if banner:
            return JsonResponse({
                "title": banner.title, 
                "text": banner.description, 
                "url": banner.url
                }, status=200)
        return JsonResponse({
                "title": None, 
                "text": None, 
                "url": None
                }, status=200)
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
    