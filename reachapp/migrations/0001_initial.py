# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('quality_score', models.PositiveSmallIntegerField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobPosting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=225)),
                ('quality_score', models.PositiveSmallIntegerField(blank=True)),
                ('description', models.TextField(max_length=1000, blank=True)),
                ('location', models.CharField(max_length=150, blank=True)),
                ('url', models.URLField(blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('employer', models.ForeignKey(to='reachapp.Employer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReachEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=225)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('jobs', models.ManyToManyField(related_name='email_jobs', to='reachapp.JobPosting')),
                ('users', models.ManyToManyField(related_name='email_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReachTracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=32)),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('is_sent', models.BooleanField(default=False)),
                ('is_opened', models.BooleanField(default=False)),
                ('is_clicked', models.BooleanField(default=False)),
                ('email', models.ForeignKey(to='reachapp.ReachEmail')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReachTrackerLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_clicked', models.BooleanField(default=False)),
                ('job', models.ForeignKey(to='reachapp.JobPosting')),
                ('tracker', models.ForeignKey(to='reachapp.ReachTracker')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='reachtracker',
            unique_together=set([('email', 'user')]),
        ),
    ]
