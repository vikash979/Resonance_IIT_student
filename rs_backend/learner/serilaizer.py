from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField
from identity_service.models import StudentInfo
from institute.models import Programs, Batches, PhaseHasSession
from subjects.models import HasSubjects, MasterSubjects

class MasterSubjectSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(MasterSubjectSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = MasterSubjects
        fields = ['url', 'background_code',]
        depth = 1

class HasSubjectsSerializer(ModelSerializer):
    image = SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(HasSubjectsSerializer, self).__init__(*args, **kwargs)

    def get_image(self, obj):
        get_master_subject = MasterSubjects.objects.get(id = obj.master_subject.id)
        return MasterSubjectSerializer(get_master_subject).data

    class Meta:
        model = HasSubjects
        fields = ['id', 'name', 'image',]
        depth = 1

class BatchSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(BatchSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Batches
        fields = ['id', 'display_name']
        depth = 1

class PhaseHasSessionSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(PhaseHasSessionSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = PhaseHasSession
        fields = ['id', 'display_name']
        depth = 1

class ProgramSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(ProgramSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Programs
        fields = ['id', 'display_name',]
        depth = 1

class StudentProfileSerializer(ModelSerializer):
    student_program = SerializerMethodField()
    current_batch = SerializerMethodField()
    phase = SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(StudentProfileSerializer, self).__init__(*args, **kwargs)

    def get_student_program(self, obj):
        program_id = obj.student_program
        program_instance = Programs.objects.get(id = program_id)
        return ProgramSerializer(program_instance).data

    def get_current_batch(self, obj):
        currnet_batch_id = obj.current_batch
        batch_instance = Batches.objects.get(id = currnet_batch_id)
        return BatchSerializer(batch_instance).data

    def get_phase(self, obj):
        phase_id = obj.phase
        phase_instance = PhaseHasSession.objects.get(id = phase_id)
        return PhaseHasSessionSerializer(phase_instance).data

    class Meta:
        model = StudentInfo
        fields = ['name', 'role_number', 'student_program', 'phase', 'current_batch', 'profile_picture',]
        depth = 1
