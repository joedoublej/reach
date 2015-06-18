#!/usr/bin/env python
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

from reachapp.views import EmailClickView, EmailEventView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^emails/(?P<tracker_code>[a-zA-Z0-9]+)/(?P<tracker_log_code>[a-zA-Z0-9]+)/$', EmailClickView.as_view(), name='click_email'),
    url(r'^events/$', csrf_exempt(EmailEventView.as_view()), name='email_event'),
    (r'^$', RedirectView.as_view(url='/admin/')),
)
