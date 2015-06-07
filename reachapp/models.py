# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models


class Employer(models.Model):

    name = models.CharField(max_length=200)
    quality_score = models.PositiveSmallIntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    name = models.CharField(max_length=225)
    quality_score = models.PositiveSmallIntegerField(blank=True)
    description = models.TextField(max_length=1000, blank=True)
    location = models.CharField(max_length=150, blank=True)
    employer = models.ForeignKey('reachapp.Employer', null=False, blank=False)
    url = models.URLField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.name, self.employer.name, self.location)

    def save(self, *args, **kwargs):
        if self.quality_score is None:
            self.quality_score = self.employer.quality_score or 0
        super(JobPosting, self).save(*args, **kwargs)


class ReachEmail(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True, help_text='Internal title to keep track of emails')
    subject = models.CharField(max_length=225, blank=True, help_text='This will be displayed e.g.: Accountant Jobs in New York, NY')
    jobs = models.ManyToManyField('reachapp.JobPosting', related_name='email_jobs')
    users = models.ManyToManyField('authtools.User', related_name='email_users')
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.subject


class ReachTracker(models.Model):
    user = models.ForeignKey('authtools.User', null=False)
    email = models.ForeignKey('reachapp.ReachEmail', null=False)
    code = models.CharField(max_length=32, unique=True)
    date_sent = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
    is_opened = models.BooleanField(default=False)
    is_clicked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('email', 'user')

    def save(self, *args, **kwargs):
        if self.is_clicked:
            self.is_opened = True
        if not self.pk:
            self.code = uuid.uuid4().hex
        super(ReachTracker, self).save(*args, **kwargs)


class ReachTrackerLog(models.Model):
    """
    Model that keeps track
    """
    user = models.ForeignKey('authtools.User', null=False)
    job = models.ForeignKey('reachapp.JobPosting', null=False)
    tracker = models.ForeignKey('reachapp.ReachTracker')
    code = models.CharField(max_length=32, unique=True)
    is_clicked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_clicked and not self.tracker.is_clicked:
            self.tracker.is_clicked = True
            self.tracker.save()
        if not self.pk:
            self.code = uuid.uuid4().hex
        super(ReachTrackerLog, self).save(*args, **kwargs)

    @property
    def affiliate_url(self):
        return 'emails/{}/{}'.format(self.tracker.code, self.code)


class ClickEvent(models.Model):
    """
    Clicks from the Mandrill event webhook
    """
    click_url = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    ip_address = models.ImageField()
    sent_timestamp = models.DateTimeField()
    user_email = models.CharField(max_length=100, null=True)


class OpenEvent(models.Model):
    """
    Opens from the Mandrill event webhook
    """
    date = models.DateTimeField(auto_now=True)
    ip_address = models.ImageField()
    sent_timestamp = models.DateTimeField()
    user_email = models.CharField(max_length=100, null=True)


class UnsubEvent(models.Model):
    """
    Unubs from the Mandrill event webhook
    """
    date = models.DateTimeField(auto_now=True)
    sent_timestamp = models.DateTimeField()
    user_email = models.CharField(max_length=100, null=True)
