
class ObjectStatusChoices(object):
    ACTIVE=0
    DELETED=1
    CHOICES = (
        (DELETED, 'Deleted'),
        (ACTIVE, 'Active')
    )


class QuestionCategoryChoices(object):
    EXERCISE=1
    DAILY_PRACTICE_PROBLEMS=2
    SOLVED_EXAMPLES = 3
    CHOICES = (
        (EXERCISE, 'Exercise'),
        (DAILY_PRACTICE_PROBLEMS, 'Daily Practice Problems'),
        (SOLVED_EXAMPLES,'Solved Examples'),
    )


class StudyMaterialChoices(object):
    NOTES=0
    VIDEO=1
    CHOICES = (
        (NOTES, 'Notes'),
        (VIDEO, 'Video'),
    )


class QuestionTypeChoices(object):
    MULTIPLE_CHOICE=1
    SINGLE_INTEGER=2
    MULTIPLE_RESPONSE=3
    FILL_IN_THE_BLANK=4
    TRUE_FALSE=5

    CHOICES = (
        (MULTIPLE_CHOICE, 'Multiple Choice Questions'),
        (SINGLE_INTEGER, 'Single Integer Questions'),
        (MULTIPLE_RESPONSE,'Multiple Response Questions'),
        (FILL_IN_THE_BLANK,'Fill in the Blanks'),
        (TRUE_FALSE,'True False')
    )



class TOCLevelChoices(object):
    UNIT=0
    CHAPTER=1
    TOPIC=2
    SUBTOPIC=3

    CHOICES = (
        (UNIT, 'Unit'),
        (CHAPTER, 'Chapter'),
        (TOPIC, 'Topic'),
        (SUBTOPIC,'Subtopic'),
    )



class AssessmentTimedChoices(object):
    ON_TOTAL = 0
    ON_QUESTION = 1

    CHOICES = (
        (ON_TOTAL, 'Timed on Total'),

        (ON_QUESTION, 'Timed on Questions'),
    )

class DifficultyLevelChoices(object):
    EASY=0
    MEDIUM=1
    HARD=2
    VERY_HARD=3
    CHOICES  = (
        (EASY, "Easy"),
        (MEDIUM, "Medium"),
        (HARD, "Hard"),
        (VERY_HARD, "Very Hard"),
    )



class AssessmentSubmissionChoices(object):
    EVERY_QUESTION=0
    ALL_QUESTIONS=1
    CHOICES  = (
        (EVERY_QUESTION, "Every Question"),
        (ALL_QUESTIONS, "All Questions"),
    )


class PublishStatusChoices(object):
    DRAFT=0
    PUBLISHED=1
    CHOICES  = (
        (DRAFT, "Draft"),
        (PUBLISHED, "Published"),
    )
