# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reachapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reachemail',
            name='title',
            field=models.CharField(help_text=b'Internal title to keep track of emails', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reachemail',
            name='subject',
            field=models.CharField(help_text=b'This will be displayed e.g.: Accountant Jobs in New York, NY', max_length=225, blank=True),
            preserve_default=True,
        ),
    ]
