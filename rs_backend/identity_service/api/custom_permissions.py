from rest_framework.permissions import BasePermission
from identity_service.models import User
from django.contrib.auth import get_user_model
from identity_service.get_user_roles import GetUserTokenByCookie

class UserCreatePermission(BasePermission):
    SAFE_METHODS = ('POST',)
    role_permissions = ('admin',)
    def has_permission(self, request, view):
        user_role_cookie_func = GetUserTokenByCookie(request)
        if user_role_cookie_func() in self.role_permissions and request.method in self.SAFE_METHODS:
            return True
        return False

class UserListPermissionReadOnly(BasePermission):
    SAFE_METHODS = ('GET', 'HEAD')
    role_permissions = ('admin',)
    def has_permission(self, request, view):
        user_role_cookie_func = GetUserTokenByCookie(request)
        print(user_role_cookie_func())
        if user_role_cookie_func() in self.role_permissions and request.method in self.SAFE_METHODS:
            return True
        return False
