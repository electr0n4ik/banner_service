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
        return False
    
    if len(token) == 16:
        token = AdminToken.objects.get(key=token)
        return True if token.user.is_superuser else False

    elif len(token) == 32:
        return True if UserToken.objects.get(key=token) else False

    return False
