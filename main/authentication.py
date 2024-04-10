from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import AdminToken, UserToken

import secrets
from rest_framework_simplejwt.tokens import RefreshToken

class BaseCustomToken:
    @classmethod
    def for_user(cls, user):
        raise NotImplementedError("Subclasses must implement for_user method")

class AdminCustomToken(BaseCustomToken):
    @classmethod
    def for_user(cls, user):
        token = secrets.token_hex(8)
        return token

class UserCustomToken(BaseCustomToken):
    @classmethod
    def for_user(cls, user):
        token = secrets.token_urlsafe(32)
        return token

class AdminTokenAuthentication(TokenAuthentication):
    model = AdminToken

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not token.user.is_staff:
            raise AuthenticationFailed('Invalid token')

        return (token.user, token)

class UserTokenAuthentication(TokenAuthentication):
    model = UserToken

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        return (token.user, token)
