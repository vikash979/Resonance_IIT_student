from django.urls import re_path
from . import api

urlpatterns = [
    re_path(r'^login/$', api.LearnerLoginAPIView.as_view(), name="LearnerLoginAPIView"),
    re_path(r'^logout/$', api.LearnerLogoutAPIView.as_view(), name="LearnerLogoutAPIView"),
    re_path(r'^profile/$', api.LearnerProfileAPIView.as_view(), name="LearnerProfileAPIView"),
    re_path(r'^dashboard/$', api.LearnerDashboardAPIView.as_view(), name="LearnerDashboardAPIView"),
]
