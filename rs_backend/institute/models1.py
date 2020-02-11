from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=50)
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField(blank=True)


class Classs(models.Model):
    # created_by =  models.IntegerField()
    name = models.CharField(max_length=120)
    display_name = models.CharField(max_length=120)
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    order = models.IntegerField()
    description = models.TextField()
    #tags = GenericRelation(Comment)


class Programs(models.Model):
    subject_choice = (
        (1, "online"),
        (2, "dist_program"),
        (3, "offline"),
    )
    name = models.CharField(max_length=120)
    display_name = models.CharField(max_length=120)
    description = models.TextField()
    type = models.IntegerField(choices=subject_choice, default=1)
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    # created_by = models.IntegerField()


class Programhasclasses(models.Model):
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    class_id = models.ForeignKey(Classs, related_name='programclassid',  on_delete=models.CASCADE)
    program = models.ForeignKey(Programs, related_name='program_list',  on_delete=models.CASCADE)


class Programclasshassubjects(models.Model):
    created_on = models.DateTimeField('created Date')
    program_has_class = models.ForeignKey(Programhasclasses, related_name='program_class', on_delete=models.CASCADE)
    class_has_subjects_id = models.IntegerField()


class Sessions(models.Model):
    YEAR_CHOICES = [(r, r) for r in range(2000, date.today().year + 1)]
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    # created_by = models.IntegerField()
    program = models.ForeignKey(Programs, related_name='programs', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    display_name = models.CharField(max_length=120)
    description = models.TextField()
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.now().year)


class SessionHasProgram(models.Model):
    # created_by =  models.IntegerField()
    session = models.ForeignKey(Sessions,related_name='sessions',  on_delete=models.CASCADE)
    program = models.ForeignKey(Programs, related_name='sessionprogram', on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=datetime.now, blank=True)


class PhaseHasSession(models.Model):
    name = models.CharField(max_length=120)
    display_name = models.CharField(max_length=120)
    description = models.TextField()
    session = models.ForeignKey(Sessions, related_name='phase_program', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_on =models.DateTimeField(default=datetime.now, blank=True)
    # created_by = models.IntegerField()


class Batches(models.Model):
    name = models.CharField(max_length=120)
    display_name = models.CharField(max_length=120)
    description = models.TextField()
    phase = models.ForeignKey(PhaseHasSession, related_name='batchphase',  on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    times_slot = models.TimeField(auto_now=False, auto_now_add=False)
    # created_by = models.IntegerField()

class StudentClassPath(models.Model):
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    ## created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # created_by = models.IntegerField()
    student_id = models.IntegerField()
    classes = models.ForeignKey(Classs, related_name='studentclasses', on_delete=models.CASCADE)
    current_choice = (
        (0, "Zero"),
        (1, "One"),
    )
    current = models.IntegerField(choices=current_choice, default='0')
    status = models.BooleanField(default=True, blank=True)

    @property
    def created(self):
        return User.objects.get(id=self.created_by)

class FacultyHasBatch(models.Model):
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    student_id = models.IntegerField()
    batches = models.ForeignKey(Batches, related_name='faculybatches', on_delete=models.CASCADE)
    faculties = models.IntegerField()