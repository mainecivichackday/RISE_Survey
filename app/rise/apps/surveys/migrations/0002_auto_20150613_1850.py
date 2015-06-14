# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='post_file',
            field=models.FileField(null=True, upload_to=b'csv', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='survey',
            name='pre_file',
            field=models.FileField(null=True, upload_to=b'csv', blank=True),
            preserve_default=True,
        ),
    ]
