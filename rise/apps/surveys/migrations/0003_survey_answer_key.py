# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_auto_20150613_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='answer_key',
            field=models.TextField(help_text=b'Answer question number and correct answer on separate lines', null=True, blank=True),
            preserve_default=True,
        ),
    ]
