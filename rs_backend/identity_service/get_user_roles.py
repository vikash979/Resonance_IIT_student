from .models import User
from rest_framework.authtoken.models import Token
from django.conf import settings

def get_role_by_dict(find_value=None, *args, **kwargs):
    for key, value in settings.USER_ROLES.items():
        if key == find_value:
            return value

class GetUserTokenByHeader:
    def __init__(self, request, *args, **kwargs):
        self.request = request

    def __call__(self, *args, **kwargs):
        pass

class GetUserTokenByCookie:
    def __init__(self, request=None, *args, **kwargs):
        self.request = request

    def __call__(self, *args, **kwargs):
        if self.request is not None:
            try:
                get_user_by_cookie_token = Token.objects.get(key=self.request.COOKIES['ur_t']).user
            except KeyError:
                return {"data": [], "status": False, "errors": True}
            else:
                get_user_role_value = Users.objects.get(user_id=get_user_by_cookie_token.id).roles
                user_role = get_role_by_dict(get_user_role_value)
                return user_role
