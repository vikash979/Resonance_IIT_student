from rest_framework import serializers
from .models import Classs, Comment, Programs, Programhasclasses, Programclasshassubjects, \
    Sessions, SessionHasProgram,PhaseHasSession, Batches, StudentClassPath, FacultyHasBatch, Target
#from django.db import transaction


class DynamicFieldsSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', set())
        super().__init__(*args, **kwargs)
        

        if fields and '__all__' not in fields:
            all_fields = set(self.fields.keys())
            for not_requested in all_fields - set(fields):
                print(not_requested)
                self.fields.pop(not_requested)
        # else:
        #     print(__name__)






class FacultyHasBatchSerializer(DynamicFieldsSerializer):

    class Meta:
        model = FacultyHasBatch
        fields = '__all__'

class BatchesSerializer(DynamicFieldsSerializer):
    faculybatches = FacultyHasBatchSerializer(many=True)

    class Meta:
        model = Batches
        fields = '__all__'


class PhaseHasSessionSerializer(DynamicFieldsSerializer):
    batchphase = BatchesSerializer(many=True)

    class Meta:
        model = PhaseHasSession
        fields = '__all__'




class SessionsSerializer(DynamicFieldsSerializer):
    #sessions_has_program = SessionHasProgramSerializer(many=True)
    #phase_session = PhaseHasSessionSerializer(many=True)

    class Meta:
        model = Sessions
        fields = '__all__'






class TargetsSerializer(DynamicFieldsSerializer):
    
    class Meta:
        model = Target
        fields = '__all__'



class ProgramsSerializer(DynamicFieldsSerializer):
   # session_programs = SessionsSerializer(many=True)
    target = TargetsSerializer()

    class Meta:
        model = Programs
        fields = '__all__'

class SessionHasProgramSerializer(DynamicFieldsSerializer):
    phase_session = PhaseHasSessionSerializer(many=True)
    session = SessionsSerializer()
    program = ProgramsSerializer()

    class Meta:
        model = SessionHasProgram
        fields = '__all__'


# class Target(DynamicFieldsSerializer):
#     target_name = ProgramsSerializer()


class ProgramclasshassubjectsSerializer(DynamicFieldsSerializer):

    class Meta:
        model = Programclasshassubjects
        fields = '__all__'

class ProgramhasclassesSerializer(serializers.ModelSerializer):
    program = ProgramsSerializer(many=False)
    program_class = ProgramclasshassubjectsSerializer(many=True)

    class Meta:
        model = Programhasclasses
        fields = '__all__'

    def get(self, instance):
        response = super().get(instance)
        response['program'] = ProgramsSerializer(instance.program).data
        return response

class SudentClassPathSerializer(DynamicFieldsSerializer):

    class Meta:
        model = StudentClassPath
        fields = '__all__'



class CommentSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        serializer = CommentSerializer(value.get_queryset()[0])
        return serializer.data



class ClasssSerializer(DynamicFieldsSerializer):
    programclassid = ProgramhasclassesSerializer(many=True)
    studentclasses = SudentClassPathSerializer(many=True)
    # tags = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Classs
        fields = '__all__'