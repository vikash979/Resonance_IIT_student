from django.contrib import admin
from .models import (
    MasterSubjects, HasSubjects, SubjectHasUnit, TopicHasContent,
    TocHasContentReleasedByFaculty, LectureHasContent,
    UnitHasChapter, ChapterHasTopic, TopicHasSubtopic
)
# Register your models here.

admin.site.register(MasterSubjects)
admin.site.register(HasSubjects)
admin.site.register(SubjectHasUnit)
admin.site.register(TopicHasContent)
admin.site.register(TocHasContentReleasedByFaculty)
admin.site.register(LectureHasContent)
admin.site.register(UnitHasChapter)
admin.site.register(ChapterHasTopic)
admin.site.register(TopicHasSubtopic)
