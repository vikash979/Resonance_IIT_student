from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.conf import settings
from datetime import date,datetime
from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

class Country(models.Model):
    country_name = models.CharField("Country Name", max_length=120)

    def __str__(self):
        return self.country_name

class Region(models.Model):
    region_name = models.CharField("Region Name", max_length=120)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    def __str__(self):
        return "{} {}".format(self.country, self.region_name)

class State(models.Model):
    state_name = models.CharField("State name", max_length=120)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.region, self.state_name)

class City(models.Model):
    city_name = models.CharField("City name", max_length=120)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.state, self.city_name)

class Center(models.Model):
    center_name = models.CharField("Center name", unique=True, max_length=120)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    status = models.BooleanField("Center status", default=False)
    created_on = models.DateTimeField("Created Date", auto_now_add=True)

    def __str__(self):
        return self.center_name

class User(AbstractUser):
    user_choice = (
        (1, "Admin"),
        (2, "Author"),
        (3, "Faculty"),
        (4, "Learner"),

    )
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=120, unique=True)
    roles = models.IntegerField(choices=user_choice)
    # objects = UserManager()
    # USERNAME_FIELD = 'name'
    # REQUIRED_FIELDS = ['name']

    # create_user function
    # create_user('username', email='..@mail.com', password='passwd', roles=int)

class StudentInfo(models.Model):
    gender_choice = (
        (1, 'Male'),
        (2, 'Female')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('Student name', max_length=120)
    email = models.EmailField("Student Email")
    phone = models.BigIntegerField("Student Mobile")
    profile_picture = models.ImageField(upload_to='student/profile/')
    dob = models.DateField()
    gender = models.IntegerField("Student Gender", default=1)
    division = models.IntegerField("division", default=0)
    role_number = models.BigIntegerField("Student role number", default=0)
    phase = models.BigIntegerField('Phase', default=0)
    phase_start_date = models.DateField('Phase start date')
    medium = models.IntegerField("medium", default=0)
    inital_batch = models.IntegerField("inital batch")
    current_batch = models.IntegerField("Current Batch")
    previous_batch = models.IntegerField("Previous Batch")
    student_class = models.IntegerField("Student Class")
    student_program = models.IntegerField("Program")
    session = models.IntegerField("Session")
    center = models.IntegerField("Center", default=0)
    father_name = models.CharField("Father name", max_length=120)
    father_email = models.EmailField("Father name")
    father_mobile = models.BigIntegerField("Father mobile")
    mother_name = models.CharField("Mother name", max_length=120)
    mother_email = models.EmailField("Mother email")
    mother_mobile = models.BigIntegerField("Mother mobile")
    status = models.BooleanField(default=False, null=True, blank=True)

class StudentHasSubjects(models.Model):
    student = models.ForeignKey(StudentInfo, on_delete=models.PROTECT)
    subject = models.IntegerField("Subject", default=0)

class Faculties(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    center = models.ForeignKey(Center, on_delete=models.PROTECT)
    # display_name = models.CharField(max_length=120)
    # description = models.TextField()
    status = models.BooleanField(default=False, null=True, blank=True)
    created_on = models.DateTimeField('created Date', auto_now_add=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Facultyhassubjects(models.Model):
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField('created Date', auto_now_add=True)
    faculty = models.ForeignKey(Faculties, on_delete=models.PROTECT)
    subject = models.IntegerField()

class Commenttag(models.Model):
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.CharField(max_length=50)
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField(blank=True)

class Studentprefs(models.Model):
    name = models.CharField(max_length=120)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    batch = models.IntegerField()
    session = models.IntegerField()
    phase = models.IntegerField()
    program = models.IntegerField()
    classId = models.IntegerField()
    created_on = models.DateTimeField('created Date')

class Studentclasspath(models.Model):
    created_on = models.DateTimeField('created Date', auto_now_add=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    current_choice = (
        ("0", "Zero"),
        ("1", "One"),
    )
    student = models.IntegerField()
    classId = models.IntegerField()
    current = models.IntegerField(choices=current_choice, default='0')

class Departments(models.Model):
    department = models.CharField('Department name', max_length=120)
    created_on = models.DateTimeField('created Date', auto_now_add=True)
    # tags = GenericRelation(Commenttag)

    def __str__(self):
        return self.department

class DepartmentMapping(models.Model):
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    user = models.ForeignKey(Faculties, on_delete=models.CASCADE)

class Designation(models.Model):
    designation = models.CharField("Designation", max_length=120)
    created_on = models.DateTimeField("Created Date", auto_now_add=True)

    def __str__(self):
        return self.designation

class DesignationMapping(models.Model):
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    user = models.ForeignKey(Faculties, on_delete=models.CASCADE)

class EmploymentType(models.Model):
    et_name = models.CharField("Employment Type Name", max_length=120)
    created_on = models.DateTimeField("Created Date", auto_now_add=True)

    def __str__(self):
        return "{}".format(self.et_name)

class EmploymentTypeMapping(models.Model):
    employment = models.ForeignKey(EmploymentType, on_delete=models.CASCADE)
    user = models.ForeignKey(Faculties, on_delete=models.CASCADE)

class UserBatch(models.Model):
    user = models.ForeignKey(Faculties, on_delete=models.CASCADE, related_name="userbatches")
    batch = models.BigIntegerField("User Batch", default=0)

    def __str__(self):
        return "{} {}".format(self.user, self.batch)

class Concept(models.Model):
    concept_name = models.CharField("Concept", max_length=20)
    concept_slug = models.SlugField("Concept slug", editable=False)

    def __str__(self):
        return self.concept_slug

    def save(self):
        self.concept_slug = slugify(self.concept_name)
        super(Concept, self).save()

class UserConcepts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='concepts')
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    created_on = models.DateTimeField("Created Date", auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.user, self.concept)

class Division(models.Model):
    division = models.CharField('Department name', max_length=120)
    created_on = models.DateTimeField('created Date', auto_now_add=True)

    def __str__(self):
        return self.division

class Skill(models.Model):
    skill = models.CharField('skill name', max_length=120)
    subject = models.IntegerField('subject')
    subject_name = models.CharField(max_length=50, blank=True, null= True)
    created_on = models.DateTimeField('created Date', auto_now_add=True)

    def __str__(self):
        return self.skill
