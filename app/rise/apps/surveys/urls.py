from django.conf.urls import patterns, url
from .views import *


# custom views
urlpatterns = patterns(
    '',
    url(r'^teachers/(?P<slug>[-\w]+)/',
        view=TeacherDetailView.as_view(),
        name="teacher-detail"),

    url(r'^teachers/$',
        view=TeacherListView.as_view(),
        name="teacher-list"),

    url(r'^surveys/upload/$',
        view=SurveyUploadView.as_view(),
        name="survey-upload"),

    url(r'^surveys/(?P<slug>[-\w\d]+)/',
        view=SurveyDetailView.as_view(),
        name="survey-detail"),

    url(r'^surveys/$',
        view=SurveyListView.as_view(),
        name="survey-list"),

    url("^$",
        view=HomepageView.as_view(),
        name="homepage"),
)
