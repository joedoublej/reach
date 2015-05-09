#!/usr/bin/env python
import smtplib

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from reachapp.models import ReachTracker, ReachTrackerLog

import logging
logger = logging.getLogger('emails')


DEFAULT_SUBJECT = 'Your job digest for today'


class ReachEmailEngine(object):

    from_address = settings.DEFAULT_FROM_EMAIL

    def __init__(self, user, email, tracker, site_domain, *args, **kwargs):
        self.user = user
        self.email_model = email
        self.email_data = {'to': user.email}
        self.email_tracker = tracker
        self.site_domain = site_domain

    def _make_subject(self, title=DEFAULT_SUBJECT):
        """
        Generate subject from title
        """
        title = self.email_model.subject or title
        if len(title) > 78:
            title = "%s..." % title[:75]
        self.email_data['subject'] = title

    def _update_tracker_link(self, job_posting):
        job_dict = job_posting.__dict__
        job_tracker_log = ReachTrackerLog.objects.create(user=self.user, job=job_posting, tracker=self.email_tracker)
        job_dict['affiliate_url'] = 'http://{}/{}'.format(self.site_domain, job_tracker_log.affiliate_url)
        job_dict['employer_name'] = job_posting.employer.name
        return job_dict

    def _get_context(self, context={}):
        """
        Fill the context
        """
        jobs = map(self._update_tracker_link, self.email_model.jobs.all())
        all_context = {
            "tid": self.email_tracker.code,
            'jobs': jobs
        }
        all_context.update(context)
        return all_context

    def render(self, template, text_template):
        """
        Render the actual email.  We use an HTML and text template in order to make a multipart message.
        """
        context = self._get_context()
        self.email_data['body'] = render_to_string(template, context)
        self.email_data['text_body'] = render_to_string(text_template, context)
        self._make_subject()

    def send(self):
        """
        Send the actual message
        """
        try:
            msg = EmailMultiAlternatives(self.email_data['subject'],
                                         self.email_data['text_body'],
                                         self.from_address,
                                         [self.email_data['to']],
                                         headers={'Reply-To': self.from_address})

            if self.email_data['body'] is not None:
                msg.attach_alternative(self.email_data['body'], "text/html")
            msg.send(fail_silently=False)
        except smtplib.SMTPException:
            logger.exception("SMTPException ocurred for user %s", self.user)
            return False
        except Exception as exc:
            logger.exception('Error sending email %s', exc.message)
            return False
        else:
            ReachTracker.objects.filter(id=self.email_tracker.id).update(is_sent=True)
            return True
