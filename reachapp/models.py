from django.db import models


class Employer(models.Model):
  name = models.CharField(max_length=200)
  date_added = models.DateTimeField(auto_now_add=True, editable=False)
  last_modified = models.DateTimeField(auto_now=True)


class JobPosting(models.Model):

  name = models.CharField(max_length=225)
  quality_score = models.IntegerField()
  description = models.CharField(max_length = 1000, blank=True, null=True)
  location = models.CharField(max_length=150, blank=True)
  employer = models.ForeignKey('reachapp.Employer')
  date_added = models.DateTimeField(auto_now_add=True, editable=False)
  last_modified = models.DateTimeField(auto_now=True)


class ReachTracker(models.Model):
  user = models.OneToOneField('auth.User', null=False)
  date_sent = models.DateTimeField(auto_now_add=True)
  is_sent = models.BooleanField(default=False)
  is_opened = models.BooleanField(default=False)
  is_clicked = models.BooleanField(default=False)


class ReachTrackerLog(models.Model):
  user = models.OneToOneField('auth.User', null=False)
  job = models.ForeignKey('reachapp.JobPosting', null=False)
  tracker = models.ForeignKey('reachapp.ReachTracker')
  is_clicked = models.BooleanField(default=False)
