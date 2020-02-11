from django.db import models
from common.models import BaseResonanceModel,TOCMapping
from common.choices import QuestionCategoryChoices,QuestionTypeChoices,AssessmentTimedChoices,\
			DifficultyLevelChoices,AssessmentSubmissionChoices,PublishStatusChoices,\
			StudyMaterialChoices
# Create your models here.


class Language(BaseResonanceModel):
    name = models.CharField(max_length=120)


class Question(BaseResonanceModel):
	
	uid = models.CharField(max_length=120,blank=True,null=True,help_text="The unique identifier of question")
	question_type = models.SmallIntegerField(choices=QuestionTypeChoices.CHOICES, default=0)
	duration_seconds = models.IntegerField(default=0)
	marks = models.FloatField(default=0)
	negative_marking = models.IntegerField(default=0)
	source = models.SmallIntegerField(choices=QuestionCategoryChoices.CHOICES, default=0)
	difficulty = models.SmallIntegerField(choices=DifficultyLevelChoices.CHOICES, default=0)
    

class QuestionStatement(BaseResonanceModel):
	question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)
	language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)
	statement = models.TextField()

class QuestionOptions(BaseResonanceModel):
	question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)
	is_correct = models.BooleanField(default=False)

class QuestionOptionsStatement(BaseResonanceModel):
	question_option = models.ForeignKey(QuestionOptions, null=True, on_delete=models.SET_NULL)
	language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)
	statement = models.TextField()
	
class QuestionOptionsExplanation(BaseResonanceModel):
	question_option = models.ForeignKey(QuestionOptions, null=True, on_delete=models.SET_NULL)
	language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)
	explanation = models.TextField()


class QuestionTOCMapping(TOCMapping):
	question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)



class Lecture(BaseResonanceModel):
	start_date_time = models.DateTimeField()
	end_date = models.DateTimeField(blank=True, null=True)
	duration_hours = models.IntegerField(default=0)
	phase_id = models.IntegerField()
	batch_id = models.IntegerField()
	faculty = models.IntegerField(default=0)
	subject = models.ForeignKey('subjects.HasSubjects', on_delete=models.CASCADE)
	room =  models.CharField(max_length=120,blank=True,null=True,help_text="The class where lecture is happening") 

class LectureTOCMapping(TOCMapping):
	lecture = models.ForeignKey(Lecture, null=True, on_delete=models.SET_NULL)

class Assessment(BaseResonanceModel):
	type = models.SmallIntegerField(choices=QuestionCategoryChoices.CHOICES, default=0)
	title =  models.CharField(max_length=120,blank=True,null=True) 
	timed_type = models.SmallIntegerField(choices=AssessmentTimedChoices.CHOICES, default=0)
	timed_duration_mins = models.IntegerField(default=0)

	#to be moved to student mapping
	#start_date = models.DateTimeField()
	#end_date = models.DateTimeField()
	
	total_marks = models.IntegerField(default=0)

	attempts_allowed = models.IntegerField(default=0)
	is_graded = models.BooleanField(default=False)
	difficulty = models.SmallIntegerField(choices=DifficultyLevelChoices.CHOICES, default=0)
	result_after = models.SmallIntegerField(choices=AssessmentSubmissionChoices.CHOICES, default=0)
	allowed_after_duedate= models.BooleanField(default=False)

class AssessmentTOCMapping(TOCMapping):
	assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
	
	
class AssessmentSection(BaseResonanceModel):
	title =  models.CharField(max_length=120,blank=True,null=True) 
	assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
	negative_marking_per_q = models.IntegerField(default=0)

class AssessmentSectionQuestion(BaseResonanceModel):
	assessment_section = models.ForeignKey(AssessmentSection, on_delete=models.CASCADE)
	negative_marking_per_q = models.IntegerField(default=0)
	question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)

class StudyMaterial(BaseResonanceModel):
	type = models.SmallIntegerField(choices=StudyMaterialChoices.CHOICES, default=0)
	title = models.CharField(max_length=120,blank=True,null=True) 
	downloadable = models.BooleanField(default=False)
	faculty_only = models.BooleanField(default=False)

class StudyMaterialFile(models.Model):
	publish_status = models.SmallIntegerField(choices=PublishStatusChoices.CHOICES, default=0)
	study_material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE,related_name="files")
	language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)
	content = models.TextField(blank=True,null=True)
	file = models.FileField(upload_to='study_material/',blank=True,null=True)


class StudyMaterialTOCMapping(TOCMapping):
	study_material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE,related_name="toc")
	
