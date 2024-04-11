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
            AdminToken.objects.create(user=user, key=token)
        except:
            pass
        return token

class UserCustomToken(BaseCustomToken):
    @classmethod
    def for_user(cls, user):
        token = secrets.token_hex(16)
        try:
            UserToken.objects.create(user=user, key=token)
        except:
            pass
        return token
