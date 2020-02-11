from django.contrib import admin
from .models import Classs, Comment, Programs, Programhasclasses, Programclasshassubjects, \
    Sessions, SessionHasProgram,PhaseHasSession, Batches, StudentClassPath, FacultyHasBatch

admin.site.register(Classs)
admin.site.register(Comment)
admin.site.register(Programs)
admin.site.register(Sessions)
admin.site.register(Programhasclasses)
admin.site.register(SessionHasProgram)
admin.site.register(PhaseHasSession)
admin.site.register(Batches)
admin.site.register(StudentClassPath)
admin.site.register(FacultyHasBatch)
admin.site.register(Programclasshassubjects)