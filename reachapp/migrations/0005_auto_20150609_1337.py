# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reachapp', '0004_auto_20150128_1326'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClickEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('click_url', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now=True)),
                ('ip_address', models.ImageField(upload_to=b'')),
                ('sent_timestamp', models.DateTimeField()),
                ('user_email', models.CharField(max_length=100, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OpenEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('ip_address', models.ImageField(upload_to=b'')),
                ('sent_timestamp', models.DateTimeField()),
                ('user_email', models.CharField(max_length=100, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnsubEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('sent_timestamp', models.DateTimeField()),
                ('user_email', models.CharField(max_length=100, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='employer',
            name='quality_score',
            field=models.PositiveSmallIntegerField(null=True),
            preserve_default=True,
        ),
    ]
