from django.db import models
from common.choices import ObjectStatusChoices,TOCLevelChoices
# Create your models here.

class ObjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(object_status=ObjectStatusChoices.ACTIVE)
        # return SoftDeleteQuerySet(self.model).filter(object_status=1,)

    def all(self):
        return super().get_queryset()


class BaseResonanceModel(models.Model):
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    object_status = models.SmallIntegerField(choices=ObjectStatusChoices.CHOICES, default=ObjectStatusChoices.ACTIVE)

    # updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,limit_choices_to={'is_staff': True})
    objects = ObjectManager()

    class Meta:
        abstract = True

class TOCMapping(BaseResonanceModel):
    level = models.SmallIntegerField(choices=TOCLevelChoices.CHOICES)
    toc_id = models.IntegerField()
    class Meta:
        abstract = True

    def get_toc_object(self):
        #get object of self.level
        #get object by id of previous line model
        pass
