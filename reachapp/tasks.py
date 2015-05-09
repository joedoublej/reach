#!/usr/bin/env python
import logging
import requests

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from xml.etree import ElementTree

from celeryapp import app
from reachapp.engine import ReachEmailEngine
from reachapp.models import Employer, JobPosting, ReachEmail, ReachTracker

logger = logging.getLogger('emails')
User = get_user_model()


@app.task
def send_email(email_id, site_domain, test=False):
    """
    For a given user, send the appropriate email
    """
    logger.debug("Starting process to send email")
    reach_email = ReachEmail.objects.get(id=email_id)

    if test:
        # Send to only superusers in the system
        users = User.objects.filter(is_superuser=True)
    else:
        users = reach_email.users

    user_ids = users.values_list('id', flat=True)

    for user_id in user_ids:
        send_email_to_user(email_id, user_id, site_domain, test=test)


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


@app.task
def fetch_jobs_from_indeed(job='job', zip_code='10011', ip_address='127.0.0.1'):
    """
    Make request to indeed.com XML feed to add to database
    """
    url_format = (
        'http://api.indeed.com/ads/apisearch?publisher=3183403411213276&v=2'
        '&format=xml&q={query}&l={zip_code}&jt=&limit=1000&fromage='
        '&filter1=&latlong=1&userip={ip_address}&radius=100'
        '&useragent=Mozilla/%2F5.0%28Chrome/42.0.2311.135'
    )
    response = requests.get(
        url_format.format(query=job, zip_code=zip_code, ip_address=ip_address)
    )
    response_xml = response.content
    root = ElementTree.fromstring(response_xml)
    for result in root.findall('./results/result'):
        job_data = parse_job_data(result)
        job_data['employer'] = _get_or_create_employer(result.find('company').text)
        job, created = JobPosting.objects.get_or_create(**job_data)
        if not created:
            logging.info("Duplicate job: {name}, Employer: {company}".format(
                name=result.find('jobtitle').text,
                company=result.find('company').text
            ))


def parse_job_data(result_dict):
    job_data = {
        'name': result_dict.find('jobtitle').text,
        'description': result_dict.find('snippet').text,
        'location': result_dict.find('formattedLocationFull').text,
        'url': result_dict.find('url').text
    }
    return job_data


def _get_or_create_employer(name):
    employer, created = Employer.objects.get_or_create(**{'name': name})
    return employer
