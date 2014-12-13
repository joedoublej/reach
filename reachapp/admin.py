# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from reachapp.models import JobPosting, Employer


class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quality_score', 'date_added')
    list_filter = ('name', 'location', 'employer__name')


class EmployerAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')
    list_filter = ('name',)


admin.site.register(JobPosting, JobPostingAdmin)
admin.site.register(Employer, EmployerAdmin)
