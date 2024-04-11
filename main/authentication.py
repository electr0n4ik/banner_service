from django.core.exceptions import ObjectDoesNotExist

from .models import AdminToken, UserToken

import secrets

class BaseCustomToken:
    @classmethod
    def for_user(cls, user):
        raise NotImplementedError("Subclasses must implement for_user method")

class AdminCustomToken(BaseCustomToken):
    @classmethod
    def for_user(cls, user):
        token = secrets.token_hex(8)
        try:
            admin_token = AdminToken.objects.get(user=user)
            return admin_token.key
        except ObjectDoesNotExist:
            AdminToken.objects.create(user=user, key=token)
        return token

class UserCustomToken(BaseCustomToken):
    @classmethod
    def for_user(cls, user):
        token = secrets.token_hex(16)
        try:
            user_token = UserToken.objects.get(user=user)
            return user_token.key
        except ObjectDoesNotExist:
            UserToken.objects.create(user=user, key=token)
        return token
