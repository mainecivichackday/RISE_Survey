# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0007_auto_20150614_0240'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='post_csv',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='survey',
            name='pre_csv',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='survey',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(allow_duplicates=False, separator=b'\'"u\\\'-\\\'"\'', blank=True, populate_from=b'\'"\\\'name\\\'"\'', editable=False, overwrite=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='teacher',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(allow_duplicates=False, separator=b'\'"u\\\'-\\\'"\'', blank=True, populate_from=b'\'"\\\'name\\\'"\'', editable=False, overwrite=False),
            preserve_default=True,
        ),
    ]
