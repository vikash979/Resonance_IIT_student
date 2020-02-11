from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path(r'^v1/auth/', include('identity_service.api.urls')),
]
