from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.MainView.as_view(), name="MainView"),
    re_path(r'^login/$', views.LoginView.as_view(), name="LoginView"),
    re_path(r'^dashboard/$', views.DashboardView.as_view(), name="DashboardView"),
    re_path(r'^faculties/$', views.FacultyView.as_view(), name="FacultyView"),
    re_path(r'^faculties/add/$', views.FacultyAddViews.as_view(), name="FacultyAddViews"),
    re_path(r'^faculties/view/$', views.FacultyViewViews.as_view(), name="FacultyViewViews"),
    re_path(r'^faculties/edit/$', views.FacultyEditViews.as_view(), name="FacultyEditViews"),
    re_path(r'^students/$', views.StudentsViews.as_view(), name="StudentsViews"),
    re_path(r'^students/add/$', views.StudentsAddViews.as_view(), name="StudentsAddViews"),
    re_path(r'^students/view/$', views.StudentsViewViews.as_view(), name="StudentsViewViews"),
    re_path(r'^students/edit/$', views.StudentsEditViews.as_view(), name="StudentsEditViews"),
    re_path(r'^master-subjects/$', views.MasterSubjectsViews.as_view(), name="MasterSubjectsViews"),
    re_path(r'^subjects/$', views.SubjectsViews.as_view(), name="SubjectsViews"),
    re_path(r'^classes/$', views.ClassViews.as_view(), name="ClassViews"),
    re_path(r'^concepts/$', views.ConceptsViews.as_view(), name="ConceptsViews"),
    re_path(r'^sessions/$', views.SessionsViews.as_view(), name="SessionsViews"),
    re_path(r'^programs/$', views.ProgramsViews.as_view(), name="ProgramsViews"),
    re_path(r'^lecture-planner/$', views.LecturePlannerView.as_view(), name="LecturePlannerView"),
    re_path(r'^phases/$', views.PhasesViews.as_view(), name="PhasesViews"),
    re_path(r'^batches/$', views.BatchesViews.as_view(), name="BatchesViews"),
    re_path(r'^centers/$', views.CentersViews.as_view(), name="CentersViews"),
    re_path(r'^divisions/$', views.DivisionsViews.as_view(), name="DivisionsViews"),
    re_path(r'^departments/$', views.DepartmentsViews.as_view(), name="DepartmentsViews"),
    re_path(r'^designations/$', views.DesignationsViews.as_view(), name="DesignationsViews"),
    re_path(r'^employements/$', views.EmployementsViews.as_view(), name="EmployementsViews"),
     re_path(r'^employements/$', views.EmployementsViews.as_view(), name="EmployementsViews"),

]
