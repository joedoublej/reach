import logging
logger = logging.getLogger('emails')

from util import task
from announcement.engines import AnnouncementEmailEngine
from announcement.models import AnnouncementLog


@task
def send_email(announcement_id, profile_id, template, text_template, context, **kwargs):
    """
    For a given user, send the appropriate email
    """
    logger.debug("Starting process to send email")
    # TODO: Add business logic to get the appropriate user

    # avoid dupe emails sent
        log, created = AnnouncementLog.objects.get_or_create(announcement_id=announcement_id, user=user)
    if not created:
        logger.warning("Should not send announcement %s to %s twice.", announcement_id, user.email)
        return
    email = AnnouncementEmailEngine(user, log)

    # Get user's city
    city_list = profile.city.all()
    if city_list:
        context['city'] = city_list[0]
    else:
        # No city will blow up in templates that use city object
        context['city'] = "Nation"
    logger.debug("Rendering and sending announcement email...")
    email.render(template, text_template, context)
    email.send()
    logger.debug("Email sent to %s", profile_id)
