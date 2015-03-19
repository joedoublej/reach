import logging
logger = logging.getLogger('emails')

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

from celeryapp import app
from reachapp.engine import ReachEmailEngine
from reachapp.models import ReachEmail, ReachTracker

@app.task
def send_email(email_id, site_domain, test=False):
    """
    For a given user, send the appropriate email
    """
    logger.debug("Starting process to send email")
    reach_email = ReachEmail.objects.get(id=email_id)

    if test:
        users = User.objects.filter(is_superuser=True)
    else:
        users = reach_email.users

    user_ids = users.values_list('id', flat=True)

    for user_id in user_ids:
        send_email_to_user.delay(email_id, user_id, site_domain, test=test)

@app.task
def send_email_to_user(email_id, user_id, site_domain, test=False):

    tracker, created = ReachTracker.objects.get_or_create(email_id=email_id, user_id=user_id)

    if not created and tracker.is_sent and not test:
        logger.warning('Resending email {} to user {}. Email not sent.'.format(email_id, user_id))
        return

    user = User.objects.get(id=user_id)
    reach_email = ReachEmail.objects.get(id=email_id)

    email = ReachEmailEngine(user, reach_email, tracker, site_domain)

    template = 'reachapp/reach_jobs1.html'
    text_template = 'reachapp/reach_jobs.txt'

    logger.debug('Rendering and sending the email...')
    email.render(template, text_template)
    sent = email.send()
    if sent:
        logger.debug('Email id {} sent to user_id {}'.format(email_id, user_id))

