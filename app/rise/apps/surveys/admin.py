from django.contrib import admin

from .models import Teacher, Survey, SurveyField, FieldResponse


admin.site.register(Teacher)
admin.site.register(Survey)
admin.site.register(SurveyField)
admin.site.register(FieldResponse)
