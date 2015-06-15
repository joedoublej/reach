# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reachapp', '0005_auto_20150609_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobposting',
            name='url',
            field=models.URLField(max_length=300, blank=True),
            preserve_default=True,
        ),
    ]
