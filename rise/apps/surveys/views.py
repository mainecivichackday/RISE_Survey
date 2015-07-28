import json
from datetime import datetime, timedelta
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic import DetailView, ListView, View, TemplateView
from django.core import serializers
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from celery.result import AsyncResult

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
        context['response_ids'] = FieldResponse.objects.filter(survey_field__survey=self.object,
                                                    survey_field__text="ResponseID")

        if self.object.pre_task_id:
            context['pre_task'] = AsyncResult(self.object.pre_task_id).state
        if self.object.post_task_id:
            context['post_task'] = AsyncResult(self.object.post_task_id).state
        return context


class SurveyReportView(views.LoginRequiredMixin,  DetailView):
    model = Survey

    def get_context_data(self, *args, **kwargs):
        context = super(SurveyReportView, self).get_context_data(*args, **kwargs)
        # Here we want to produce some basic report data
        context['questions'] = self.object.answers
        context['field_responses'] = {}
        context['response_ids'] = FieldResponse.objects.filter(survey_field__survey=self.object,
                                                               survey_field__text="ResponseID")

        context['results'] = {'Q1': "70%", 'Q2': '65%'}
        context['common_correct'] = ['Q1', 'Q8']
        context['common_wrong'] = ['Q2']
        context['report'] = True

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

    def get_success_url(self):
        return reverse('survey-list')

    def get_context_data(self, *args, **kwargs):
        context = super(SurveyUploadView, self).get_context_data(*args, **kwargs)
        return context

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        form.save()
        return super(SurveyUploadView, self).form_valid(form)


