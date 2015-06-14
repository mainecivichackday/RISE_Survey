# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0006_auto_20150614_0227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='survey',
            old_name='task_id',
            new_name='post_task_id',
        ),
        migrations.AddField(
            model_name='survey',
            name='pre_task_id',
            field=models.CharField(max_length=255, null=True, blank=True),
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
