import json

from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.core.cache import cache
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import (ValidationError, 
                                       APIException,)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from . import models
# from .func import create_periodic_task
from .authentication import (AdminCustomToken,
                             UserCustomToken)

from .permissions import (AdminCustomTokenPermission,
                          UserCustomTokenPermission,)


class TokenCreateView(TokenObtainPairView):
    permission_classes = [AllowAny]
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

    def post(self, request, format=None):
        user = None
        try:
            is_admin = request.data.get('is_admin', False)
            login_user = request.data.get('username', None)
            password_user = request.data.get('password', False)

            if not login_user or not password_user:
                raise ValidationError({
                    'error': 'Username and password are required'})

            existing_user = User.objects.filter(username=login_user).exists()

            if existing_user:
                user = authenticate(request, 
                                    username=login_user, 
                                    password=password_user)

                refresh_token = AdminCustomToken if user.is_superuser else UserCustomToken
                refresh = refresh_token.for_user(user)

                description_response = "admin_token" if user.is_superuser else "user_token"
                login(request, user)
                return Response({
                    "detail": "Account was found",
                    description_response: str(refresh)
                })
                

            if is_admin:
                user = User.objects.create_superuser(username=login_user, 
                                                     password=password_user)
                login(request, user)
                refresh = AdminCustomToken.for_user(user)
                return Response({
                    "detail": "admin_created",
                    "admin_token": str(refresh)})
            else:
                user = User.objects.create_user(username=login_user, 
                                                password=password_user)
                login(request, user)
                refresh = UserCustomToken.for_user(user)
                return Response({
                    "detail": "user_created",
                    "user_token": str(refresh)})


        except Exception as e:
            raise APIException({
                "error": e})


class UserBannerView(APIView):
    permission_classes = [AdminCustomTokenPermission, 
                          UserCustomTokenPermission]

    def get(self, request):
        tag_id: str = request.GET.get("tag_id", None)
        feature_id: str = request.GET.get("feature_id", None)
        use_last_revision: bool = True if request.GET.get(
            "use_last_revision").lower() == "true" else False
        
        if not tag_id or not feature_id:
            err_text: str = "Does not exist tag_id" if not tag_id \
                else "Does not exist feature_id" if not feature_id \
                else "Does not exist ids"
            return JsonResponse(
                    {"Incorrect data": err_text},
                    safe=False,
                    status=400)
        
        if 1:  # use_last_revision:
            banner = models.Banner.objects.all()
        else:
            banners_data = json.loads(cache.get('banners'))
            for banner_data in banners_data:
                if int(feature_id) == banner_data['feature_id'] and \
                    int(tag_id) in banner_data['tag_ids']:
                    return JsonResponse({
                        "title": banner_data.get("title"), 
                        "text": banner_data.get("description"), 
                        "url": banner_data.get("url")
                        }, status=200)
                
            return JsonResponse({
                "error": "Banner for this feature and tag not found!"
            }, status=404)
        
        if tag_id:
            banner = banner.filter(tag_ids__contains=[int(tag_id)])

        if feature_id:
            banner = banner.filter(feature_id=int(feature_id))
        
        banner = banner.filter(is_active=True)
        if banner:
            return JsonResponse({
                "title": banner.first().title, 
                "text": banner.first().description, 
                "url": banner.first().url
                }, status=200)
        else:
            return JsonResponse({
                "error": "Banner for this feature and tag not found!"
            }, status=404)


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
                "Добавить сюда вывод одного баннера! Или нет баннера"],  #TODO:
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

        data = json.loads(request.body.decode('utf-8'))
        tag_ids = data.get("tag_ids")
        feature_id = data.get("feature_id")
        content = data.get("content")
        is_active = data.get("is_active")

        try:
            banner = models.Banner.objects.create(
                feature_id=feature_id,\
                tag_ids=tag_ids,
                title=content.get("title"),
                description=content.get("text"),
                url=content.get("url"),
                is_active=is_active
            )

            return JsonResponse({
                "method": request.method,
                "banner_id": banner.id
                },
                status=201)
        
        except ValueError as e:
            return JsonResponse(
                {"Incorrect data, exception:": f"{e}"},
                status=400)
        
        except IntegrityError as e:
            return JsonResponse(
                {"Incorrect data, exception:": f"{e}"},
                status=400)
    
    else:
        return JsonResponse({
            'error': 'Method not allowed'
            }, status=405)


@csrf_exempt
def banner_view(request, id):
    if request.method == 'PATCH':
        data = json.loads(request.body.decode('utf-8'))

        if not id:
            "Некорректные данные"
            return JsonResponse({
                "error": "Missing banner_id in request data"}, status=400)

        try:
            banner = models.Banner.objects.get(id=id)
        except models.Banner.DoesNotExist:
            "Баннер не найден"
            return JsonResponse({
                "error": f"Banner with id {id} does not exist"}, status=404)

        tag_ids = data.get("tag_ids", None)
        feature_id = data.get("feature_id", None)
        content = data.get("content", None)
        is_active = data.get("is_active", None)

        if tag_ids:
            banner.tag_ids = tag_ids

        if feature_id:
            banner.feature_id = feature_id

        if content:
            banner.title = content.get("title", banner.title)
            banner.description = content.get("text", banner.description)
            banner.url = content.get("url", banner.url)
        
        if is_active:
            banner.is_active = is_active

        try:
            banner.save()
            return JsonResponse("OK", safe=False, status=200)
        except IntegrityError as e:
            "Некорректные данные, дубликат"
            return JsonResponse(
                {"Incorrect data, exception:": f"{e}"},
                status=400
            )
    
    elif request.method == 'DELETE':
        if not id:
            "Некорректные данные"
            return JsonResponse({
                "error": "Missing banner_id in request data"}, status=400)

        try:
            banner = models.Banner.objects.get(id=id)
        except models.Banner.DoesNotExist:
            "Баннер не найден"
            return JsonResponse({
                "error": f"Banner with id {id} does not exist"}, status=404)
        
        banner.delete()
        return JsonResponse({
            "content": f"Banner id={id} delete!"
            }, status=204)
    
    else:
        return JsonResponse({
            'error': 'Method not allowed'
            }, status=405)
    