# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from reachapp.tasks import fetch_jobs


class Command(BaseCommand):
    help = 'Hits the Indeed API and adds new jobs'

    def handle(self, *args, **options):
        fetch_jobs()
