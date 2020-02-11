from django.urls import re_path
from . import api

urlpatterns = [
    re_path(r'^demo/$', api.DemoAPIView.as_view(), name="DemoAPIView"),
    re_path(r'^login/$', api.UserAuthenticationAPIView.as_view(), name="UserAuthenticationAPIView"),
    re_path(r'^create/$', api.FacultyAPIVIew.as_view(), name="FacultyAPIVIew"),
    re_path(r'^list/$', api.ListUsersListAPIView.as_view(), name="ListUsersListAPIView"),
    re_path(r'^roles/$', api.UserRolesAPIView.as_view(), name="UserRolesAPIView"),
    re_path(r'^designation/$', api.DesignationAPIView.as_view(), name="DesignationAPIView"),
    re_path(r'^employement-type/$', api.EmployementTypeAPIView.as_view(), name="EmployementTypeAPIView"),
    re_path(r'^department/$', api.DepartmentAPIView.as_view(), name="DepartmentAPIView"),
    re_path(r'^division/$', api.DivisionAPIView.as_view(), name="DivisionAPIView"),
    re_path(r'^skill/$', api.SkillAPIView.as_view(), name="SkillAPIView"),
    re_path(r'^faculty/$', api.FacultyAPIVIew.as_view(), name="FacultyAPIVIew"),
    re_path(r'^student/$', api.StudentAPIView.as_view(), name="StudentAPIView"),
    re_path(r'^centers/$', api.CenterAPIView.as_view(), name='CenterAPIView'),
    re_path(r'^country/$', api.CountryListAPIView.as_view(), name="CountryListAPIView"),
    re_path(r'^country/(?P<country>\d+)/$', api.RegionListAPIView.as_view(), name="RegionListAPIView"),
    re_path(r'^country/(?P<country>\d+)/(?P<region>\d+)/$', api.StateListAPIView.as_view(), name="StateListAPIView"),
    re_path(r'^country/(?P<country>\d+)/(?P<region>\d+)/(?P<state>\d+)/$', api.CityListAPIView.as_view(), name="CityListAPIView"),
    re_path(r'^country/(?P<country>\d+)/(?P<region>\d+)/(?P<state>\d+)/(?P<city>\d+)/$', api.CenterListAPIView.as_view(), name="CenterListAPIView"),
]
