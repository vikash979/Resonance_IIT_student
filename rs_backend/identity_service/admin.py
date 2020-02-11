from django.contrib import admin
from django.contrib.auth.models import Group
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    Departments, Faculties, Facultyhassubjects, Studentprefs,
    Studentclasspath, User, UserBatch, Region,
    Country, State, City, Center, Designation, EmploymentType,
    Concept, UserConcepts, Division, Skill, DesignationMapping,
    DepartmentMapping, EmploymentTypeMapping, StudentInfo,
    StudentHasSubjects
)

# class UsersInline(admin.StackedInline):
#     model = Users
#     can_delete = False
#     list_display = ()
#     list_filter = ()
#     search_fields = ()
#     ordering = ()
#     filter_horizontal = ()
#     verbose_name_plural = 'Users'
#
# class UserAdmin(BaseUserAdmin):
#     inlines = (UsersInline,)

admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(Departments)
admin.site.register(Faculties)
admin.site.register(StudentInfo)
admin.site.register(StudentHasSubjects)
admin.site.register(Facultyhassubjects)
admin.site.register(Studentprefs)
admin.site.register(Studentclasspath)
admin.site.register(DesignationMapping)
admin.site.register(DepartmentMapping)
admin.site.register(EmploymentTypeMapping)
admin.site.register(UserBatch)
admin.site.register(Region)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Center)
admin.site.register(Designation)
admin.site.register(EmploymentType)
admin.site.register(Concept)
admin.site.register(UserConcepts)
admin.site.register(Division)
admin.site.register(Skill)
