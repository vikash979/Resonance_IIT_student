from django.db import models
from identity_service.models import User
from datetime import date,datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType


class MasterSubjects(models.Model):
    name = models.CharField(max_length=120)
    short_code = models.CharField(max_length=20)
    url = models.ImageField(upload_to='subjects/')
    background_code = models.CharField(max_length=10, default='#0000FF')
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class HasSubjects(models.Model):
    subject_choice = (
        (1, "One"),
        (2, "Two"),
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    class_id = models.IntegerField(blank=True, null=True)
    class_name = models.CharField(max_length=50,blank=True,null=True)
    master_subject = models.ForeignKey(MasterSubjects,on_delete=models.CASCADE)
    # subject_optional  = models.IntegerField(choices = subject_choice,default = 1)
    code = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SubjectHasUnit(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    order = models.IntegerField()
    book_id = models.IntegerField()
    label = models.CharField(max_length=200)


class UnitHasChapter(models.Model):
    order = models.BigIntegerField(default=0)
    label = models.CharField(max_length=255)
    subject_has_unit_id = models.ForeignKey(HasSubjects, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_on = models.DateField(auto_now_add=True)

class ChapterHasTopic(models.Model):
    order = models.BigIntegerField(default=0)
    label = models.CharField(max_length=255)
    unit_has_chapter_id = models.ForeignKey(UnitHasChapter, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_on = models.DateField(auto_now_add=True)

class TopicHasSubtopic(models.Model):
    order = models.IntegerField(default=0)
    label = models.CharField(max_length=255)
    level = models.PositiveSmallIntegerField(default=0)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_on = models.DateField(auto_now_add=True)

class SubjectHasUnit(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    label = models.CharField(max_length=255)
    order = models.IntegerField()
    book_id = models.IntegerField()

class TopicHasContent(models.Model):
    content_choice = (
        (1, "notes"),
        (2, "video"),
        (3, "assessments"),
    )

    topic_level_choice = (
        (1, "unit"),
        (2, "chapter"),
        (3, "chapter"),
        (4, "sub-topics"),
    )

    toc_id = models.BigIntegerField(default=0)
    toc_level = models.IntegerField(choices=topic_level_choice, default=0)
    content_id = models.BigIntegerField(default=0)
    content_type = models.IntegerField(choices=content_choice, default=0)
    faculty_releasable = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_on = models.DateField(auto_now_add=True)

class TocHasContentReleasedByFaculty(models.Model):
    toc_has_content_id = models.ForeignKey(TopicHasContent, null=True, on_delete=models.SET_NULL)
    batch_id = models.BigIntegerField(default=0)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_on = models.DateField(auto_now_add=True)

class LectureHasContent(models.Model):
    lecture_id = models.BigIntegerField(default=0)
    toc_has_content_id = models.ForeignKey(TopicHasContent, null=True, on_delete=models.SET_NULL)
