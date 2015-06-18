#!/usr/bin/env python
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from reachapp.events import handle_event
from reachapp.models import ReachTrackerLog


class EmailClickView(View):

    def get(self, request, tracker_code, tracker_log_code):
        log = ReachTrackerLog.objects.filter(code=tracker_log_code).get()
        if not log.is_clicked:
            log.is_clicked = True
            log.save()
        return HttpResponseRedirect(log.job.url)


class EmailEventView(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(EmailEventView, self).dispatch(*args, **kwargs)

    def head(self, request):
        """
        for Mandrill verification
        """
        return HttpResponse()

    def post(self, request, *args, **kwargs):
        """
        this is for the event webhook
        """
        event = request.POST.get('mandrill_events', {})
        handle_event(event)
        return HttpResponse()
