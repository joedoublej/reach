from __future__ import unicode_literals

import logging

from reachapp.models import ClickEvent, OpenEvent, UnsubEvent

logger = logging.getLogger('default')


def handle_click(event):
    ts = event.get('ts')
    url = event.get('url')
    ip_address = event.get('ip')
    message = event.get('msg', {'email': None})
    user_email = message.get('email')

    ClickEvent.objects.create(
        click_url=url,
        ip_address=ip_address,
        sent_timestamp=ts,
        user_email=user_email
    )


def handle_open(event):
    ts = event.get('ts')
    ip_address = event.get('ip')
    message = event.get('msg', {'email': None})
    user_email = message.get('email')

    OpenEvent.objects.create(
        ip_address=ip_address,
        sent_timestamp=ts,
        user_email=user_email
    )


def handle_unsub(event):
    ts = event.get('ts')
    ip_address = event.get('ip')
    message = event.get('msg', {'email': None})
    user_email = message.get('email')

    UnsubEvent.objects.create(
        ip_address=ip_address,
        sent_timestamp=ts,
        user_email=user_email
    )


HANDLERS = {
    'click': handle_click,
    'open': handle_open,
    'unsub': handle_unsub
}


def handle_event(event):
    event_type = event.get('event')
    handler = HANDLERS.get(event_type)
    if handler is None:
        logger.info('Unknown event: {}'.format(event_type))
        return
    handler(event)
