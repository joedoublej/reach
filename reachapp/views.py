#!/usr/bin/env python
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.views.generic.base import View

from reachapp.models import ReachTrackerLog


class EmailClickView(View):

    def get(self, request, tracker_code, tracker_log_code):
        log = ReachTrackerLog.objects.filter(code=tracker_log_code).get()
        if not log.is_clicked:
            log.is_clicked = True
            log.save()
        return HttpResponseRedirect(log.job.url)
