from django.db.models import Q
from django.utils.encoding import force_unicode
import csv
from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django_extensions.db.models import TimeStampedModel, AutoSlugField
from django.template.defaultfilters import slugify

from .utils import generate_slug, sanitize
from .tasks import import_csv_data


class Teacher(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=255)
    slug = AutoSlugField(populate_from='name')
    email  = models.EmailField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.name)


class Survey(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=255)
    slug = AutoSlugField(populate_from='name')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    pre_file = models.FileField(upload_to='csv', blank=True, null=True)
    post_file = models.FileField(upload_to='csv', blank=True, null=True)
    pre_csv = models.TextField(blank=True, null=True)
    post_csv = models.TextField(blank=True, null=True)
    answer_key = models.TextField(blank=True, null=True,
                                  help_text="Answer question number and correct\
                                             answer on separate lines")
    pre_task_id = models.CharField(blank=True, null=True, max_length=255)
    post_task_id = models.CharField(blank=True, null=True, max_length=255)

    def __unicode__(self):
        return u'{0}'.format(self.name)

    @permalink
    def get_absolute_url(self):
        return ('survey-detail', None, {'slug': self.slug})

    @property
    def answers(self):
        if self.answer_key:
            keys = self.answer_key.split('\r\n')
            answers = {}
            for key in keys:
                if key: q, a = key.split('=')
                answers[int(q)] = int(a)
            return answers
        return {}

    @property
    def questions(self):
        ''' Returns a list of SurveyField instances which are
            the questions in the Pre Survey Responses '''
        qlist = []
        # Use the answer key to dig questions out of the field responses
        for question_number in self.answers.keys():
            result = self.surveyfield_set.filter(qualtrics_id='Q'+str(question_number))
            if len(result) > 0:
                qlist.append(result[0])
        return qlist

    def question_responses(self, respondant_id=False, pre=False, post=False):
        '''
        Given a respondant id, returns all the question answers by that respondants
        for the given state. By default we return the Pre state
        '''
        respondant_answers = {}

        if respondant_id:
            filters = Q(respone_id=respondant_id)
        else:
            filters = Q()
        for q in self.questions:
            responses = q.fieldresponse_set.filter(filters,
                                                   is_pre=pre,
                                                   is_post=post)
            if len(responses) > 0:
                respondant_answers[int(q.qualtrics_id.replace('Q', ''))] = responses[0].response
        return respondant_answers


    @property
    def pre_responses(self, q=None):
        return FieldResponse.objects.filter(survey_field__in=self.questions,
                                            is_pre=True)

    @property
    def post_responses(self):
        return FieldResponse.objects.filter(survey_field__in=self.questions,
                                            is_post=True)

    def save(self, *args, **kwargs):
        super(Survey, self).save(*args, **kwargs)

        if self.pre_file or self.pre_csv:
            self.pre_task_id = import_csv_data.delay(self, SurveyField, FieldResponse, mode="pre").task_id
        if self.post_file or self.post_csv:
            self.post_task_id = import_csv_data.delay(self, SurveyField, FieldResponse, mode="post").task_id

        super(Survey, self).save()


class SurveyField(TimeStampedModel):
    survey = models.ForeignKey(Survey)
    qualtrics_id = models.CharField(_("Qualtrics ID"), max_length=255)
    text = models.TextField(_("Question Text"), blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.text)

class FieldResponse(TimeStampedModel):
    teacher = models.ForeignKey(Teacher, blank=True, null=True)
    respone_id = models.CharField(max_length=255, blank=True, null=True)
    survey_field = models.ForeignKey(SurveyField)
    response = models.TextField(blank=True, null=True)
    is_pre = models.BooleanField(default=False)
    is_post = models.BooleanField(default=False)

    @property
    def responses(self):
        #columns = Q(survey_field__text='ResponseID')|Q(survey_field__text='Name')| \
        #          Q(survey_field__text='StartDate')|Q(survey_field__text='Grade')
        return FieldResponse.objects.filter(respone_id=self.respone_id,
                                            is_pre=self.is_pre, is_post=self.is_post)

    def __unicode__(self):
        return u'{0}'.format(self.response)
