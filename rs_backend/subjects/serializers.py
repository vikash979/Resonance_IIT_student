from rest_framework.serializers import ModelSerializer
from .models import *


class MasterSubjectSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(MasterSubjectSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = MasterSubjects
        fields = '__all__'
        depth = 1

class HasSubjectSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(HasSubjectSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = HasSubjects
        fields = '__all__'
        depth = 1

# class SubjectHasUnitSerializer(ModelSerializer):
#     def __init__(self, *args, **kwargs):
#         super(SubjectHasUnitSerializer, self).__init__(*args, **kwargs)
#
#     class Meta:
#         model = SubjectHasUnit
#         fields = '__all__'
#         depth = 1
#
# class UnitHasChapterSerializer(ModelSerializer):
#     def __init__(self, *args, **kwargs):
#         super(UnitHasChapterSerializer, self).__init__(*args, **kwargs)
#
#     class Meta:
#         model = UnitHasChapter
#         fields = '__all__'
#         depth = 1
#
# class ChapterHasTopicSerializer(ModelSerializer):
#     def __init__(self, *args, **kwargs):
#         super(ChapterHasTopicSerializer, self).__init__(*args, **kwargs)
#
#     class Meta:
#         model = ChapterHasTopic
#         fields = '__all__'
#         depth = 2
#
# class TopicHasSubtopicSerializer(ModelSerializer):
#     def __init__(self, *args, **kwargs):
#         super(TopicHasSubtopicSerializer, self).__init__(*args, **kwargs)
#
#     class Meta:
#         model = TopicHasSubtopic
#         fields = '__all__'
#         depth = 1
#
# class TopicHasContentSerializer(ModelSerializer):
#     def __init__(self, *args, **kwargs):
#         super(TopicHasContentSerializer, self).__init__(*args, **kwargs)
#
#     class Meta:
#         model = TopicHasContent
#         fields = '__all__'
#         depth = 1
