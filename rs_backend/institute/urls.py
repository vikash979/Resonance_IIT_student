#from institute.views import ClasssViewset
from rest_framework.routers import DefaultRouter
from institute import views
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
#from django.views.generic.base import TemplateView
from django.conf.urls import url
from . import views
# from institute.views import BatchesView
# from rest_framework import renderers SessionHasProgramViewset

app_name = 'institute'




urlpatterns = [
  
url(r'^institutes/$', views.ClasssViewset.as_view({'get': 'list', 'post': 'create'}), name='institutes'),
url(r'^program/$', views.ProgramsViewset.as_view({'get': 'list', 'post': 'create'}), name='program'),
url(r'^programhasclasses/$', views.ProgramhasclassesViewset.as_view({'get': 'list', 'post': 'create'}), name='programhasclasses'),
url(r'^programclasshassubjects/$', views.ProgramclasshassubjectsViewset.as_view({'get': 'list', 'post': 'create'}), name='programclasshassubjects'),
url(r'^sessions/$', views.SessionsViewset.as_view({'get': 'list', 'post': 'create'}), name='batches'),
url(r'^phasehassession/$', views.PhaseHasSessionViewset.as_view({'get': 'list', 'post': 'create'}), name='phasehassession'),
url(r'^batches/$', views.BatchesView.as_view({'get': 'list', 'post': 'create'}), name='batches'),
url(r'^student_cl_view/$', views.StudentClassPathView.as_view({'get': 'list', 'post': 'create'}), name='student_cl_view'),
url(r'^faculty_has_batch/$', views.FacultyHasBatchView.as_view({'get': 'list', 'post': 'create'}), name='faculty_has_batch'),
url(r'^session_has_program/$', views.SessionHasProgramViewset.as_view({'get': 'list', 'post': 'create'}), name='faculty_has_batch'),
url(r'^program_target/$', views.TargetProgramViewset.as_view({'get': 'list', 'post': 'create'}), name='faculty_has_batch'),
    #post_list = BatchesView.as_view({'post': 'create'})


]
