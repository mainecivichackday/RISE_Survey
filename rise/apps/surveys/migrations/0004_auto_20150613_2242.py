# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0003_survey_answer_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldresponse',
            name='is_post',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fieldresponse',
            name='is_pre',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
