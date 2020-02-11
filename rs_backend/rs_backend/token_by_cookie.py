from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import TokenAuthentication
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.authentication import BasicAuthentication

def get_token_from_header(request):
    auth = request.META.get('HTTP_AUTHORIZATION', None)
    if isinstance(auth, str):
        auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth
    msg = _('Invalid token header. No credentials provided.')
    raise exceptions.AuthenticationFailed(msg)

class TokenByHeadersAuthentication:
    keyword = 'ur_t'
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token

    def authenticate_header_token(self, request):
        auth = get_token_from_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials_key(token)

    def authenticate_credentials_key(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (token.user, token)

class TokenByCookieAuthentication(TokenAuthentication):
    def authenticate(self, request):
        if isinstance(request.META.get('HTTP_COOKIE'), str):
            data = request.META.get('HTTP_COOKIE')
            coming_data = dict(a.split("=") for a in data.split(";"))
            key = coming_data.get('ur_t') or coming_data.get(' ur_t')
            if key:
                return self.authenticate_credentials(key)
            else:
                a = TokenByHeadersAuthentication()
                key = a.authenticate_header_token(request)
                if key:
                    return self.authenticate_credentials(key[1])
                raise exceptions.AuthenticationFailed(_('Invalid token.'))

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (token.user, token)
