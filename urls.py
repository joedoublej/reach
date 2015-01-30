from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

from reachapp.views import EmailClickView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^emails/(?P<tracker_code>[a-zA-Z0-9]+)/(?P<tracker_log_code>[a-zA-Z0-9]+)/$', EmailClickView.as_view(), name='click_email'),
    (r'^$', RedirectView.as_view(url='/admin/')),
)
