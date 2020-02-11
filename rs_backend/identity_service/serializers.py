from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import (
    User, Departments, Designation, EmploymentType, Concept,
    UserConcepts, UserBatch, Region, Country, State, City,
    Center, DepartmentMapping, DesignationMapping, EmploymentTypeMapping,
    Division, Skill, Faculties, StudentInfo, StudentHasSubjects
)

class UsersModelSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(UsersModelSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        exclude = ('password',)
        depth = 1

class FacultiesSerializer(ModelSerializer):
    user = UsersModelSerializer()
    def __init__(self, *args, **kwargs):
        super(FacultiesSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Faculties
        fields = '__all__'
        depth = 5

class DepartmentSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(DepartmentSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Departments
        fields = '__all__'
        depth = 1

class DesignationSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(DesignationSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Designation
        fields = '__all__'
        depth = 1

class EmploymentTypeSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(EmploymentTypeSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = EmploymentType
        fields = '__all__'
        depth = 1

class ConceptSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(ConceptSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Concept
        fields = '__all__'
        depth = 1

class UserConceptSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(UserConceptSerializer, self).__init__(*args, **kwargs)

    class Meta:
        models = UserConcepts
        fields = '__all__'
        depth = 1

class UserBatchSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(UserBatchSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = UserBatch
        fields = '__all__'
        depth = 1

class RegionSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(RegionSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Region
        fields = '__all__'
        depth = 1

class CountrySerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CountrySerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Country
        fields = '__all__'
        depth = 1

class StateSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(StateSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = State
        fields = '__all__'
        depth = 1

class CitySerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CitySerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = City
        fields = '__all__'
        depth = 1

class CenterSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CenterSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Center
        fields = '__all__'
        depth = 4

class DivisionSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(DivisionSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Division
        fields = '__all__'
        depth = 1

class SkillSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(SkillSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Skill
        fields = '__all__'
        depth = 1

class DepartmentMappingSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(DepartmentMappingSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = DepartmentMapping
        fields = '__all__'
        depth = 1

class DesignationMappingSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(DesignationMappingSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = DesignationMapping
        fields = '__all__'
        depth = 1

class EmploymentTypeMappingSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(EmploymentTypeMappingSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = EmploymentTypeMapping
        fields = '__all__'
        depth = 1

class StudentInfoSerializer(ModelSerializer):
    center = SerializerMethodField()
    def __init__(self, *args, **kwargs):
        super(StudentInfoSerializer, self).__init__(*args, **kwargs)

    def get_center(self, obj):
        print(obj.center)
        a = Center.objects.get(id = obj.center)
        return CenterSerializer(a).data

    class Meta:
        model = StudentInfo
        exclude = ('user',)
        depth = 1

# class FacultyInfoSerializer(ModelSerializer):
#     center = SerializerMethodField()
#     def __init__(self, *args, **kwargs):
#         super(FacultyInfoSerializer, self).__init__(*args, **kwargs)

#     def get_center(self, obj):
#         print(obj.center)
#         a = Center.objects.get(id = obj.center)
#         return CenterSerializer(a).data

#     class Meta:
#         model = Faculties
#         exclude = ('user',)
#         depth = 1

class StudentInfoSerializerOnly(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(StudentInfoSerializerOnly, self).__init__(*args, **kwargs)

    class Meta:
        model = StudentInfo
        exclude = ('user',)
        depth = 1

class StudentHasSubjectSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(StudentHasSubjectSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = StudentHasSubjects
        fields = '__all__'
        depth = 1
