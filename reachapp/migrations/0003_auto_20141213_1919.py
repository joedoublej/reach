# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reachapp', '0002_reachtracker_reachtrackerlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPosting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=225)),
                ('quality_score', models.IntegerField()),
                ('description', models.CharField(max_length=1000, null=True, blank=True)),
                ('location', models.CharField(max_length=150, blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('employer', models.ForeignKey(to='reachapp.Employer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='job',
            name='employer',
        ),
        migrations.AlterField(
            model_name='reachtrackerlog',
            name='job',
            field=models.ForeignKey(to='reachapp.JobPosting'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Job',
        ),
    ]
