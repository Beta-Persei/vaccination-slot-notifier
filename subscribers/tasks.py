from datetime import datetime, timedelta

from django.conf import settings

from subscribers.models import Subscriber
from vaccination_slot_notifier import celery_app
from subscribers.utils import check_and_notify_subscriber


@celery_app.task
def check_available_slots():
    subscriber_list = Subscriber.objects.filter(
        active=True,
        last_mail_sent__lt=datetime.now()
        - timedelta(seconds=settings.MAIL_COOLDOWN_SECONDS),
    )
    for subscriber in subscriber_list:
        check_and_notify_subscriber(subscriber)


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        settings.SNIFFING_INTERVAL_SECONDS, check_available_slots.s()
    )
