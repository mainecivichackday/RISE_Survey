# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0004_auto_20150613_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldresponse',
            name='teacher',
            field=models.ForeignKey(blank=True, to='surveys.Teacher', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='survey',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(allow_duplicates=b'"\'False\'"', separator=b'\'"u\\\'-\\\'"\'', blank=True, populate_from=b'\'"\\\'name\\\'"\'', editable=False, overwrite=b'"\'False\'"'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='teacher',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(allow_duplicates=b'"\'False\'"', separator=b'\'"u\\\'-\\\'"\'', blank=True, populate_from=b'\'"\\\'name\\\'"\'', editable=False, overwrite=b'"\'False\'"'),
            preserve_default=True,
        ),
    ]
