#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from reachapp.models import ReachTracker

import logging
logger = logging.getLogger('emails')


DEFAULT_SUBJECT = 'Your jobs'

class ReachEmailEngine(object):

  from_address = settings.DEFAULT_FROM_EMAIL

   def __init__(self, user, log, *args, **kwargs):
        self.user = user
        self.email_data = {'to': user.email}
        self.email_log = log

    def _make_subject(self, title=DEFAULT_SUBJECT):
        """
        Generate subject from title
        """
        if len(title) > 78:
            title = "%s..." % title[:75]
        self.email_data['subject'] = title

    def _get_context(self, context):
        """
        Fill the context
        """
        all_context = {
            "rid": self.email_log.code
        }
        all_context.update(context)
        return all_context

    def render(self, template, text_template, context):
        """
        Render the actual email.  We use an HTML and text template in order to make a multipart message.
        """
        context = self._get_context(context)
        self.email_data['body'] = render_to_string(template, context)
        self.email_data['text_body'] = render_to_string(text_template, context)
        self._make_subject(context['subject'])

    def send(self):
        """
        Send the actual message
        """
        # if self.user.unsubscribed:
        #     return

        try:
            msg = EmailMultiAlternatives(self.email_data['subject'], self.email_data['text_body'], self.from_address, [self.email_data['to']], headers={'Reply-To': self.from_address})
            msg.attach_alternative(self.email_data['body'], "text/html")
            msg.send(fail_silently=False)
        except smtplib.SMTPException:
            logger.exception("SMTPException ocurred for user %s", self.user)
            return False
        else:
            ReachTracker.objects.filter(id=self.email_log.id).update(is_sent=True)
            return True
