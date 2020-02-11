"""rs_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'', include('admin_frontend.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('identity_service.urls')),
    path('api/v1/l/', include('learner.api.urls')),
    path('api/v1/subject/',include('subjects.urls')),
    path('api/v1/institute/',include('institute.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
