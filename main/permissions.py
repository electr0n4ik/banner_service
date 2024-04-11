from datetime import timedelta

from django.utils import timezone

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

from .models import AdminToken, UserToken


class AdminCustomTokenPermission(BasePermission):
    def has_permission(self, request, view):
        return validate_custom_token(request)


class UserCustomTokenPermission(BasePermission):
    def has_permission(self, request, view):
        return validate_custom_token(request)


def validate_custom_token(request):
    token = request.headers.get('Authorization')
    if not token:
        raise AuthenticationFailed('Укажите токен')

    if len(token) == 16:
        token = AdminToken.objects.filter(key=token)
        if token and token.first().expiration_time < timezone.now() - \
            timedelta(hours=0.01):
            token.delete()
            raise AuthenticationFailed('Токен истек')
        elif token:
            return True if token.first().user.is_superuser else False
        else:
            raise AuthenticationFailed('Токена не существует, создайте новый')
    elif len(token) == 32:
        token = UserToken.objects.filter(key=token)
        if token and token.first().expiration_time < timezone.now() - \
            timedelta(hours=1):
            token.delete()
            raise AuthenticationFailed('Токен истек')
        elif token:
            return True if token else False
        else:
            raise AuthenticationFailed('Токена не существует, создайте новый')
