from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def user_banner_view(request):
    if request.method == 'GET':
        return JsonResponse({
            "content":"Получение баннера для пользователя"
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
    