from django.core.urlresolvers import reverse
import floppyforms as forms

from .models import Survey


class SurveyForm(forms.ModelForm):
    #meditation = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Survey
        exclude = ['user', 'slug', 'pre_task_id', 'post_task_id']

