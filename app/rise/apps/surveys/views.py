import json
from datetime import datetime, timedelta
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic import DetailView, ListView, View, TemplateView
from django.core import serializers
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from .models import Teacher, Survey, FieldResponse
from .forms import SurveyForm
from braces import views


class UserRestrictedMixin(object):

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return self.model.objects.filter(user=self.request.user.id)
        return self.model.objects.all()


class TeacherDetailView(DetailView):
    model = Teacher


class TeacherListView(UserRestrictedMixin, ListView):
    model = Teacher



class HomepageView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomepageView, self).get_context_data(*args, **kwargs)
        return context


class SurveyDetailView(views.LoginRequiredMixin,  DetailView):
    model = Survey

    def get_context_data(self, *args, **kwargs):
        context = super(SurveyDetailView, self).get_context_data(*args, **kwargs)
        # We want the responses from the survey loaded in a dict on a per-row basis
        context['field_responses'] = {}
        response_ids = FieldResponse.objects.filter(survey_field__survey=self.object,
                                                    survey_field__text="ResponseID")
        print response_ids
        for resp in response_ids:
            fields = FieldResponse.objects.filter(survey_field__survey=self.object, respone_id=resp.respone_id)
            context['field_responses'][resp.respone_id] = resp.response

        return context

class SurveyListView(views.LoginRequiredMixin,  ListView):
    model = Survey

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return Survey.objects.filter(user=self.request.user.id)
        return Survey.objects.all()

class SurveyUploadView(views.LoginRequiredMixin,  CreateView):
    model = Survey
    form_class = SurveyForm


    def get_context_data(self, *args, **kwargs):
        context = super(SurveyUploadView, self).get_context_data(*args, **kwargs)
        meditation = None

        try:
            meditation = Teacher.objects.get(slug=self.request.GET.get('meditation'))
        except:
            pass

        context['meditation'] = meditation
        return context


    def get_success_url(self):
        return reverse('homepage', args=()) + '#about'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        form.save()
        return super(SurveyUploadView, self).form_valid(form)


