# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from authtools.admin import NamedUserAdmin


from reachapp.forms import UserCreationForm
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
        send_email_task(reach_email.id, site_domain)


def send_test_email(modeladmin, request, queryset):
    site_domain = get_current_site(request).domain
    for reach_email in queryset:
        send_email_task(reach_email.id, site_domain, test=True)

class EmailAdmin(admin.ModelAdmin):

    list_display = ('subject', 'date_added')
    exclude = ('date_added',)
    search_fields = ['jobs__name', 'users__name']
    filter_horizontal = ('users', 'jobs', )
    actions = [send_email, send_test_email]


admin.site.register(JobPosting, JobPostingAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(ReachEmail, EmailAdmin)

User = get_user_model()

class UserAdmin(NamedUserAdmin):
    """
    A UserAdmin that sends a password-reset email when creating a new user,
    unless a password was entered.
    """
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'description': (
                "Enter the new user's email address and click save."
                " The user username will be set to their email and a default password"
                " will be set."
            ),
            'fields': ('email', 'name',),
        }),
        ('Password', {
            'description': "Optionally, you may set the user's password here.",
            'fields': ('password1', 'password2'),
            'classes': ('collapse', 'collapse-closed'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change and not obj.has_usable_password():
            # We set password so that we can save the user model
            obj.set_password(settings.DEFAULT_PASSWORD)

        super(UserAdmin, self).save_model(request, obj, form, change)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
