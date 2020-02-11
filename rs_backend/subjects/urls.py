from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^master_subject/$', views.MasterSubjectApiView.as_view(), name="MasterSubjectApiView"),
    re_path(r'^has_subject/$', views.HasSubjectApiView.as_view(), name="HasSubjectApiView"),
    re_path(r'^subject_has_unit/$', views.SubjectHasUnitApiView.as_view(), name="SubjectHasUnitApiView"),
    re_path(r'^unit_has_chapter/$', views.UnitHasChapterApiView.as_view(), name="UnitHasChapterApiView"),
    re_path(r'^chapter_has_topic/$', views.ChapterHasTopicApiView.as_view(), name="ChapterHasTopicApiView"),
    re_path(r'^topic_has_subtopic/$', views.TopicHasSubtopicApiView.as_view(), name="TopicHasSubtopicApiView"),
    re_path(r'^topic_has_content/$', views.TopicHasContentApiView.as_view(), name="TopicHasContentApiView"), 
]