# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse

from reachapp.models import JobPosting, Employer, ReachEmail
from reachapp.tasks import send_email as send_email_task


class JobPostingAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'quality_score', 'date_added')
    list_filter = ['name', 'location', 'employer__name']
    list_per_page = 200

class EmployerAdmin(admin.ModelAdmin):

    list_display = ['id', 'name']
    list_filter = ['name']


def send_email(modeladmin, request, queryset):
    site_domain = get_current_site(request).domain
    for reach_email in queryset:
        send_email_task.delay(reach_email.id, site_domain)


def send_test_email(modeladmin, request, queryset):
    site_domain = get_current_site(request).domain
    for reach_email in queryset:
        send_email_task.delay(reach_email.id, site_domain, test=True)

class EmailAdmin(admin.ModelAdmin):

    list_display = ('subject', 'date_added')
    exclude = ('date_added',)
    search_fields = ['jobs__name', 'users__name']
    filter_horizontal = ('users', 'jobs', )
    actions = [send_email, send_test_email]


admin.site.register(JobPosting, JobPostingAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(ReachEmail, EmailAdmin)
