from django.utils.encoding import force_unicode
import csv
from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django_extensions.db.models import TimeStampedModel
from django.template.defaultfilters import slugify


def sanitize(str=''):
    return unicode(str.replace('/', ''), 'iso-8859-1')


class Teacher(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(blank=True)
    email  = models.EmailField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Teacher, self).save(*args, **kwargs)


class Survey(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    pre_file = models.FileField(upload_to='csv', blank=True, null=True)
    post_file = models.FileField(upload_to='csv', blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.name)

    @permalink
    def get_absolute_url(self):
        return ('survey-detail', None, {'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Survey, self).save(*args, **kwargs)

        self.import_csv_data()

    def import_csv_data(self):
        path = self.pre_file.path
        data = [row for row in csv.reader(open(path, 'r'))]
        # throw away the first two headers
        ids = data.pop(0)
        names = data.pop(0)
        for row in data:
            index = 0
            for f in row:
                try:
                    text = sanitize(names[index])
                    qid = ids[index]
                except IndexError:
                    pass
                print qid
                if text and qid:
                    field, _created = SurveyField.objects.get_or_create(survey=self,
                                                                        text=text,
                                                                        qualtrics_id=qid)
                    response = FieldResponse.objects.create(teacher=Teacher.objects.all()[0],
                                                            respone_id=row[index],
                                                            survey_field=field,
                                                            response=f)
                    response.save()
                    print 'Added {0} {1}'.format(qid, response)
                    index += 1

class SurveyField(TimeStampedModel):
    survey = models.ForeignKey(Survey)
    qualtrics_id = models.CharField(_("Qualtrics ID"), max_length=255)
    text = models.TextField(_("Question Text"), blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.text)

class FieldResponse(TimeStampedModel):
    teacher = models.ForeignKey(Teacher)
    respone_id = models.CharField(max_length=255, blank=True, null=True)
    survey_field = models.ForeignKey(SurveyField)
    response = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.response)
