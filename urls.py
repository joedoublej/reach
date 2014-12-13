from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', RedirectView.as_view(url='/admin/')),
)

# if settings.LOCAL:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
