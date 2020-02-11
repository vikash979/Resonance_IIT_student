from django.contrib import admin
from .models import (
    Lecture, LectureTOCMapping
)
# Register your models here.

admin.site.register(Lecture)
admin.site.register(LectureTOCMapping)
