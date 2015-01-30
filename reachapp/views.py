from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View

from reachapp.models import ReachTracker, ReachTrackerLog

class EmailClickView(View):

  def get(self, request, tracker_code, tracker_log_code):
    log = ReachTrackerLog.objects.filter(code=tracker_log_code).get()
    if not log.is_clicked:
      log.is_clicked = True
      log.save()
    return HttpResponseRedirect(log.job.url)
